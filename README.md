# Dialogflow Fulfillment Translation Sample for Python (Flask)
==============================================================
## Setup Instructions

### Dialogflow Setup
 1. Create an account on Dialogflow
 1. Create a new Dialogflow agent
 1. Restore the `dialogflow-agent.zip` ZIP file in the root of this repo
   1. Go to your agent's settings and then the *Export and Import* tab
   1. Click the *Restore from ZIP* button
   1. Select the `dialogflow-agent.zip` ZIP file in the root of this repo
   1. Type *RESTORE* and and click the *Restore* button

### Fulfillment Setup
 1. Click on the Google Cloud project ID in your agent's setting to open the Google Cloud console
 1. Enable the [Google Cloud Translation API](http://console.cloud.google.com/apis/library/translate.googleapis.com/)
 1. [Create an API key](https://cloud.google.com/docs/authentication/api-keys#creating_an_api_key) and copy the value into the `API_KEY` varible in `main.py` and save the file
 1. Run `pip install -r requirements.txt`
 1. Deploy fulfillment to App Engine
   1. [Download and authenticate the Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstart-macos)
   1. Run `gcloud app deploy`, make a note of the service URL, which will be used in the next step
 1. Set the fulfillment URL in Dialogflow to your App Engine service URL
   1. Go to your [agent's fulfillment page](https://console.dialogflow.com/api-client/#/agent//fulfillment)
   1. Click the switch to enable webhook for your agent
   1. Enter you App Engine service URL and append `/webhook` (e.g. `https://translate-10929.appspot.com/webhook`) to the URL field
   1. Click *Save* at the bottom of the page

## How to report bugs
* If you find any issues, please open a bug here on GitHub

## How to make contributions?
Please read and follow the steps in the CONTRIBUTING.md

## License
See LICENSE.md

## Terms
Your use of this sample is subject to, and by using or downloading the sample files you agree to comply with, the [Google APIs Terms of Service](https://developers.google.com/terms/) and the [Dialogflow's Terms of Use and Privacy Policy](https://dialogflow.com/terms/).