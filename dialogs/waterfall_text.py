from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    NumberPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    AttachmentPrompt,
    PromptOptions,
    PromptValidatorContext,
    DateTimePrompt,
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState

from data_models import UserProfile
import datetime

class WaterfallText(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(WaterfallText, self).__init__(dialog_id or WaterfallText.__name__)
            
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    #self.what_step,
                    self.fatturatestuale_step,
                    self.date_step,
                    self.confirm_step,
                    self.summary_step,
                ],
            )
        )
        #self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(TextPrompt(TextPrompt.__name__, WaterfallText.insertCorrectdate))
        self.add_dialog(
            NumberPrompt(NumberPrompt.__name__)
        )
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            AttachmentPrompt(
                AttachmentPrompt.__name__, WaterfallText.picture_prompt_validator
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__
    
    async def what_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text(f"Ciao, cosa vuoi fare?"),
                choices=[Choice("Fattura testuale"), Choice("Fattura visiva"), Choice("Query")],
            ),
        )

    async def fatturatestuale_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Per favore inserisci l'importo")),
        )
        return step_context.next(0)

    
    async def date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        step_context.values["amount"] = step_context.result
        self.var = True
        return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Per favore inserisci la data (DD-MM-YYYY)"),
                    retry_prompt=MessageFactory.text("Inserisci la data corretta (DD-MM-YYYY)"),)
            )


    async def confirm_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["date"] = step_context.result
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text(f"Hai inserito l'importo: {step_context.values['amount']}€ nella data: {step_context.values['date']} è corretto?")),
        )


    async def insertdata_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        if step_context.result:
           return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Bella bro")),
            )
        return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Cap e cazz")),
            )

    async def summary_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        return await step_context.end_dialog()

    @staticmethod
    async def picture_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        if not prompt_context.recognized.succeeded:
            await prompt_context.context.send_activity(
                "No attachments received. Proceeding without a profile picture..."
            )

            # We can return true from a validator function even if recognized.succeeded is false.
            return True

        attachments = prompt_context.recognized.value

        valid_images = [
            attachment
            for attachment in attachments
            if attachment.content_type in ["image/jpeg", "image/png"]
        ]

        prompt_context.recognized.value = valid_images

        # If none of the attachments are valid images, the retry prompt should be sent.
        return len(valid_images) > 0


    @staticmethod
    async def insertCorrectdate(prompt_context: PromptValidatorContext) -> bool:
        try:
            datetime.datetime.strptime(prompt_context.recognized.value, "%d-%m-%Y")
        except ValueError:
            return False
        
        return True