# OwnGPT

Wassist allows you to contact GPT3 directly from WhatsApp and not only that. Wassist also allows you to save your own personal data and later search and retrieve it using GPT3 to generate a response. In the examples folder you can see several examples of how to use this bot so you don't have to remember anything ever again.


## Supported Features

* **No-Command**: This is the default mode. The bot will respond to any message you send it through the GPT3 regular completion API.

* **Commands**: This mode is activated by sending the bot a message starting with the command character. The default command character is /. 
    * Currently supported commands:
        * /h: Show a help message that lists all the commands
        * /s <message>: Save the message to the database
        * /q <question>: Ask a question about the database and get a response from GPT3.
        * /f <message>: Find related messages in the database.
        * /w: Get weather forecast from [IMS](https://ims.gov.il/he).
        * Send audio file for transcripting (Multi languages).
        * d/ <message>: Draw using Dall-E.
        * /c: Get OpenAI estimated costs
            * Today.
            * Yesterday.
            * Last 7 days.
            * Last 30 days.

## Components and Frameworks used in WAssist
* [Loguru](https://pypi.org/project/loguru/) For logging.
* [FastAPI](https://github.com/tiangolo/fastapi) For Whatsapp webhhoks.
* [ma-nish](https://pypi.org/project/ma-nish/) Whatsapp Cloud API client.
* [weatheril](https://pypi.org/project/weatheril/) For Weather forecst.
* [OpenAI](https://pypi.org/project/openai/) OpenAI client for ChatGPT, Dall-E and Whisper.



## How to use WAssist
Wassist can be installed and run as a system service or as a Docker containerm.

1. open Whatsapp cloud api with Meta and creat apllication. read **[Here](https://pypi.org/project/ma-nish/)** how to do it.
2. Set the following environment variables:
    * [TOKEN](https://developers.facebook.com/docs/whatsapp/business-management-api/get-started#1--acquire-an-access-token-using-a-system-user-or-facebook-login)= #Whatsapp API Token
    * PHONE_NUMBER_ID= #Whatsapp phone number ID
    * [VERIFY_TOKEN](https://developers.facebook.com/docs/graph-api/webhooks/getting-started#configure-webhooks-product)= #Token for whatsapp token verification
    * OPENAI_KEY= #OpenAPI API key
    * ALLOWED_NUMBERS= #List of numbers allowed to communicate with the bot, comma separated values.




