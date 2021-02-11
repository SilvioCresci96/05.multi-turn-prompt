# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

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

import datetime


class WaterfallPhoto(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(WaterfallPhoto, self).__init__(dialog_id or WaterfallPhoto.__name__)

        #self.user_profile_accessor = user_state.create_property("UserProfile")

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.domanda_step,
                    self.summary_step,
                ],
            )
        )
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        #self.add_dialog(TextPrompt(TextPrompt.__name__, WaterfallQuery.insertCorrectdate))
        self.add_dialog(
            NumberPrompt(NumberPrompt.__name__)
        )
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            AttachmentPrompt(
                AttachmentPrompt.__name__, WaterfallPhoto.picture_prompt_validator
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__
    
    async def domanda_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Cosa vuoi sapere?")),
        )
        return step_context.next(0)

    
   

    async def summary_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        return await step_context.end_dialog()

    
