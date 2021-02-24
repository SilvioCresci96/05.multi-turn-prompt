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

from io import BytesIO

import requests
import FormRecognizer
import datetime


class WaterfallPhoto(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(WaterfallPhoto, self).__init__(dialog_id or WaterfallPhoto.__name__)

        #self.user_profile_accessor = user_state.create_property("UserProfile")

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.picture_step,
                    self.confirm_step,
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

    
    async def picture_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        prompt_options = PromptOptions(
            prompt=MessageFactory.text(
                "Please attach a profile picture (or type any message to skip)."
            ),
            retry_prompt=MessageFactory.text(
                "The attachment must be a jpeg/png image file."
            ),
        )
        return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)

    async def confirm_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        if step_context.result:
            image = step_context.result[0]
        res: Response = requests.get(image.content_url)

        dati_scontrino = FormRecognizer.runAnalysis(input_file = BytesIO(res.content), file_type = image.content_type)

        if dati_scontrino is None:
            await step_context.context.send_activity("C'è stato un problema")
            return await step_context.end_dialog()
        
        step_context.values["dati_scontrino"] = dati_scontrino

        # WaterfallStep always finishes with the end of the Waterfall or
        # with another dialog; here it is a Prompt Dialog.
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text(f"Dalla foto ho rilevato l'importo {dati_scontrino['totale']}€ in data {dati_scontrino['data']}")),
        )

    async def evaluate_data_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        if step_context.result:
            pass 
        else:
            await step_context.context.send_activity("Prova a reinviare la foto")
            await step_context.replace_dialog(WaterfallDialog.__name__)


    async def summary_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        #FormRecognizer.main([r"C:\Users\silvi\Desktop\Università\Cloud\test\1.jpeg"])
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

    
