#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "9a9a6891ae794fc7b09f71570531e6cb")
    LUIS_APP_ID = os.environ.get("LuisAppId", "80c3205c-c993-4229-a124-d93bfa0a050b")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "08c35c22af9d4eefa96a62a31592ed1f")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com")
    
