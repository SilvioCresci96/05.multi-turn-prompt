from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
import requests

from .cancel_and_help_dialog import CancelAndHelpDialog


class CancellaDialogo(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(CancellaDialogo, self).__init__(dialog_id or CancellaDialogo.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.date_step,
                    self.result_step,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        If a destination city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        invoice_details = step_context.options

        if invoice_details.date is None and invoice_details.periodo is None:
            message_text = "Di quale giorno desideri eliminare la fattura (DD-MM-YYYY)?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(invoice_details.date)

    async def result_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        If an origin city has not been provided, prompt for one.
        :param step_context:
        :return DialogTurnResult:
        """
        invoice_details = step_context.options

        # Capture the response to the previous step's prompt
        invoice_details.date = step_context.result
        
        r = requests.get(f"https://mybillbotfirstfunction.azurewebsites.net/api/first_function?id_utente={step_context.context.activity.from_property.id}&funct=cancellaFattura&data={invoice_details.date}")

        if r.text is not None and r.text != "":
            await step_context.context.send_activity(f"Hai eliminato la fattura in data {invoice_details.date}")
        else:
            await step_context.context.send_activity(f"In data {invoice_details.date} già non erano presenti fatture")

            
        return await step_context.end_dialog()

