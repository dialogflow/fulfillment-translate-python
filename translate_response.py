#!/usr/bin/env python
# Copyright 2017 Google Inc.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is a sample for a translation fulfillment webhook for an API.AI agent

This is meant to be used with the sample translate agent for API.AI, it uses
the Google Cloud Translation API and requires an API key from an API project
with the Google Cloud Translation API enabled.
"""

_TRANSLATE_W = [
    u'Sure. What do you want to translate and into which language?',
    u'Okay. Just tell me what you need to translate and into which language.',
    u'No problem. What are we translating, and into which language?',
    u'All right. What do you need translated, and into which language?'
]

_TRANSLATE_INTO_W = [
    u'Which language would you like to translate this into?',
    u'Okay. What language are you trying to translate into?',
    u'Which language did you want this translated into?',
    u'Just tell me what language you want this translated into.'
]

_TRANSLATE_W_FROM = [
    u'Sure thing. Just tell me what you want to translate from {lang}.',
    u'Absolutely. I can translate from {lang}.'
    u' What would you like to translate?',
    u'I am familiar with {lang}.'
    u' Let me know what you need to translate from it.',
    u'Easy enough. What do you want to translate from {lang}?'
]

_TRANSLATE_W_TO = [
    u'Sure thing. Just tell me what you want to translate into {lang}.',
    u'Absolutely. I can translate into {lang}.'
    u' What would you like to translate?',
    u'I am familiar with {lang}. Let me know what you need to translate.',
    u'Easy enough. What do you want to translate into {lang}?'
]

_TRANSLATE_W_FROM_TO = [
    u'Sure thing. Just tell me what you want to translate from'
    u' {lang_from} into {lang_to}.',
    u'Absolutely. I can translate from {lang_from} into {lang_to}.'
    u' What would you like to translate?',
    u'Of course! I can translate from {lang_from} into {lang_to}.'
    u' Just let me know what you need to translate.',
    u'Easy enough.'
    u' What do you want to translate from {lang_from} into {lang_to}?',
]

_TRANSLATE_UNKNOWN_LANGUAGE = [
    u'Sorry, I couldn\'t find a translation into this language.',
    u'Unfortunately this language is unfamiliar to me.'
    u' I wasn\'t able to get a translation.',
    u'I\'m not too familiar with this language.'
    u' I wasn\'t able to translate that.',
    u'Sorry. I haven\'t learned this language yet.'
]

_TRANSLATE_RESULT = [
    u'Here is how that translates from {fromLang} into {toLang}: {text}.',
    u'Here is the translation from {fromLang} into {toLang}: {text}.',
    u'Okay, I translated that from {fromLang} into {toLang} for you: {text}.',
    u'That translates from {fromLang} to {toLang} like so: {text}.',
]

_TRANSLATE_NETWORK_ERROR = [
    u'Sorry, the translation service is not responding.'
    u' Let\'s try again in a bit.',
    u'I can\'t connect to the translation service now.'
    u' Sorry about this. Let\'s retry in a minute.',
    u'Seems like there\'s a connection problem with the translation service.'
    u' Let\'s give a moment and try again.',
    u'Looks like the translation service isn\'t responding right now.'
    u' We can try again in a moment if you like.'
]

_TRANSLATE_ERROR = [
    u'I\'m not quite sure what happened,'
    u' but I was unable to get translation at this time.',
    u'Sorry, I ran into an unexpected problem while trying'
    u' to get a translation. Let\'s try that again.',
    u'I\'m sorry. I wasn\'t able to complete that translation for some reason.'
    u' Let\'s try again in a moment.',
    u'Looks like something went wrong in the middle of that translation.'
    u' Better try that again.',
    u'I\'m not sure what happened,'
    u' but I wasn\'t able to finish translating that.'
    u' We may need to try that again.'
]
