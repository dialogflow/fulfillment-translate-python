#!/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is a sample for a translation fulfillment webhook for an Dialogflow agent

This is meant to be used with the sample translate agent for Dialogflow, it uses
the Google Cloud Translation API and requires an API key from an API project
with the Google Cloud Translation API enabled.
"""

import json
import random
from http.client import HTTPException
from urllib.error import HTTPError, URLError

from flask import Flask, jsonify, make_response, request
from googleapiclient.discovery import build

from language_list import _LANGUAGE_CODE_LIST as language_code_dict
from language_list import _LANGUAGE_LIST as language_dict
from translate_response import (_TRANSLATE_ERROR, _TRANSLATE_INTO_W,
                                _TRANSLATE_NETWORK_ERROR, _TRANSLATE_RESULT,
                                _TRANSLATE_UNKNOWN_LANGUAGE, _TRANSLATE_W,
                                _TRANSLATE_W_FROM, _TRANSLATE_W_FROM_TO,
                                _TRANSLATE_W_TO)

# API key to access the Google Cloud Translation API
# 1. Go to console.google.com create or use an existing project
# 2. Enable the Cloud Translation API in the console for your project
# 3. Create an API key in the credentials tab and paste it below
API_KEY = '<PASTE_API_KEY_HERE>'
TRANSLATION_SERVICE = build('translate', 'v2', developerKey=API_KEY)

app = Flask(__name__)
log = app.logger


@app.route('/webhook', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook

    This is meant to be used in conjunction with the translate Dialogflow agent
    """

    # Get request parameters
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')

    # Check if the request is for the translate action
    if action == 'translate.text':
        # Get the parameters for the translation
        text = req['queryResult']['parameters'].get('text')
        source_lang = req['queryResult']['parameters'].get('lang-from')
        target_lang = req['queryResult']['parameters'].get('lang-to')

        # Fulfill the translation and get a response
        output = translate(text, source_lang, target_lang)

        # Compose the response to Dialogflow
        res = {'fulfillmentText': output,
               'outputContexts': req['queryResult']['outputContexts']}
    else:
        # If the request is not to the translate.text action throw an error
        log.error('Unexpected action requested: %s', json.dumps(req))
        res = {'speech': 'error', 'displayText': 'error'}

    return make_response(jsonify(res))


def translate(text, source_lang, target_lang):
    """Returns a string containing translated text, or a request for more info

    Takes text input, source and target language for the text (all strings)
    uses the responses found in translate_response.py as templates
    """

    # Validate the languages provided by the user
    source_lang_code = validate_language(source_lang)
    target_lang_code = validate_language(target_lang)

    # If both languages are invalid or no languages are provided tell the user
    if not source_lang_code and not target_lang_code:
        response = random.choice(_TRANSLATE_UNKNOWN_LANGUAGE)

    # If there is no text but two valid languages ask the user for input
    if not text and source_lang_code and target_lang_code:
        response = random.choice(_TRANSLATE_W_FROM_TO).format(
            lang_from=language_code_dict[source_lang_code],
            lang_to=language_code_dict[target_lang_code])

    # If there is no text but a valid target language ask the user for input
    if not text and target_lang_code:
        response = random.choice(_TRANSLATE_W_TO).format(
            lang=language_code_dict[target_lang_code])

    # If there is no text but a valid source language assume the target
    # language is English if the source language is not English
    if (not text and
        source_lang_code and
        source_lang_code != 'en' and
            not target_lang_code):
        target_lang_code = 'en'

    # If there is no text, no target language and the source language is English
    # ask the user for text
    if (not text and
        source_lang_code and
        source_lang_code == 'en' and
            not target_lang_code):
        response = random.choice(_TRANSLATE_W_FROM).format(
            lang=language_code_dict[source_lang_code])

    # If there is no text and no languages
    if not text and not source_lang_code and not target_lang_code:
        response = random.choice(_TRANSLATE_W)

    # If there is text but no languages
    if text and not source_lang_code and not target_lang_code:
        response = random.choice(_TRANSLATE_INTO_W)

    # If there is text and a valid target language but no source language
    if text and not source_lang_code and target_lang_code:
        response = translate_text(text, source_lang_code, target_lang_code)

    # If there is text and 2 valid languages return the translation
    if text and source_lang_code and target_lang_code:
        response = translate_text(text, source_lang_code, target_lang_code)

    # If no response is generated from the any of the 8 possible combinations
    # (3 booleans = 2^3 = 8 options) return an error to the user
    if not response:
        response = random.choice(_TRANSLATE_ERROR)

    return response


def translate_text(query, source_lang_code, target_lang_code):
    """returns translated text or text indicating a translation/network error

    Takes a text to be translated, source language and target language code
    2 letter ISO code found in language_list.py
    """

    try:
        translations = TRANSLATION_SERVICE.translations().list(
            source=source_lang_code,
            target=target_lang_code,
            q=query
        ).execute()
        translation = translations['translations'][0]
        if 'detectedSourceLanguage' in translation.keys():
            source_lang_code = translation['detectedSourceLanguage']
        resp = random.choice(_TRANSLATE_RESULT).format(
            text=translation['translatedText'],
            fromLang=language_code_dict[source_lang_code],
            toLang=language_code_dict[target_lang_code])
    except (HTTPError, URLError, HTTPException):
        resp = random.choice(_TRANSLATE_NETWORK_ERROR)
    except Exception:
        resp = random.choice(_TRANSLATE_ERROR)
    return resp


def validate_language(language):
    """returns 2 letter language code if valid, None if language is invalid

    Uses dictionary in language_list.py to verify language is valid
    """

    try:
        lang_code = language_dict[language]
    except KeyError:
        lang_code = None
    return lang_code

if __name__ == '__main__':
    PORT = 8080

    app.run(
        debug=True,
        port=PORT,
        host='0.0.0.0'
    )
