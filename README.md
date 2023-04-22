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
