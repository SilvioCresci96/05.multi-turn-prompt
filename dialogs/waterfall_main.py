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
from dialogs.waterfall_query import WaterfallQuery
from dialogs.waterfall_text import WaterfallText
import datetime

class WaterfallMain(ComponentDialog):
    def __init__(self, user_state: UserState):
        super(WaterfallMain, self).__init__(WaterfallMain.__name__)
    
        self.user_profile_accessor = user_state.create_property("UserProfile")
        
        self.add_dialog(WaterfallQuery(WaterfallQuery.__name__))
        self.add_dialog(WaterfallText(WaterfallText.__name__))

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.what_step,
                    self.summary_step,
                ],
            )
        )
        
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        

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


    async def summary_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        result = step_context.result.value
        await step_context.context.send_activity(MessageFactory.text(result))

        if result == "Fattura testuale":
            return await step_context.begin_dialog(WaterfallText.__name__)
        else:
            return await step_context.replace_dialog(WaterfallMain.__name__)

        return await step_context.end_dialog()    


    