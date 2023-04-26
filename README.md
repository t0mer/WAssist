# WAssist

Wassist allows you to contact GPT3 directly from WhatsApp and not only that. Wassist also allows you to save your own personal data and later search and retrieve it using GPT3 to generate a response. In the examples folder, you can see several examples of how to use this bot so you don't have to remember anything ever again.


## Supported Features

* **No-Command**: This is the default mode. The bot will respond to any message you send it through the GPT3 regular completion API.

* **Commands**: This mode is activated by sending the bot a message starting with the command character. The default command character is /. 
    * Currently supported commands:
        * /h: Show a help message that lists all the commands
        * /s <message>: Save the message to the database
        * /q <question>: Ask a question about the database and get a response from GPT3.
        * /f <message>: Find related messages in the database.
        * /w: Get weather forecast from [IMS](https://ims.gov.il/he).
        * Send audio file for transcription (Multi-languages).
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
* [OpenAI](https://pypi.org/project/openai/) OpenAI client for ChatGPT, Dall-E, and Whisper.



## How to use WAssist
Wassist can be installed and run as a system service or a Docker container.

1. open Whatsapp cloud API with Meta and creat an application. read **[Here](https://pypi.org/project/ma-nish/)** how to do it.
2. Set the following environment variables:
    * [TOKEN](https://developers.facebook.com/docs/whatsapp/business-management-api/get-started#1--acquire-an-access-token-using-a-system-user-or-facebook-login)= #Whatsapp API Token
    * PHONE_NUMBER_ID= #Whatsapp phone number ID
    * [VERIFY_TOKEN](https://developers.facebook.com/docs/graph-api/webhooks/getting-started#configure-webhooks-product)= #Token for whatsapp token verification
    * OPENAI_KEY= #OpenAPI API key
    * ALLOWED_NUMBERS= #List of numbers allowed to communicate with the bot, comma-separated values.
3. If you want to run WAssist as a ***docker container***, copy the following code into your docker-compose.yaml:
    ```yaml
    version: "3.6"
    services:
    wassist:
        image: techblog/wassist
        container_name: Wassist
        restart: always
        ports:
        - 80:7020
        environment:
        - TOKEN= #Whatsapp API Token
        - PHONE_NUMBER_ID= #Whatsapp phone number ID
        - VERIFY_TOKEN= #Token for whatsapp token verification
        - OPENAI_KEY= #OpenAPI API key
        - ALLOWED_NUMBERS= #List of numbers allowed to communicate with the bot, comma-separated values.
        volumes:
        - ./wassist:/app/data
    ```
    **Make sure to set all the environment variables before running the *"docker-compose up -d"* command.
    
    
4. If you want to run WAssist as a systemd service, clone the repository using the following command:
    ```bash
    git clone https://github.com/t0mer/WAssist
    ```
    enter the *Wassist* folder and install the dipendencies:
    ```bash
    pip3 install -r requirements.txt
    ```

    Next, create a file names **"wassist.service"** under **/etc/systemd/system"** and paste the following content:

    ```bash
    [Unit]
    Description=GPT Whatsapp 
    After=network-online.target
    Wants=network-online.target systemd-networkd-wait-online.service
    StartLimitIntervalSec=5
    StartLimitBurst=5

    [Service]
    EnvironmentFile=/etc/environment
    KillSignal=SIGINT
    WorkingDirectory=/opt/dev/OwnGPT/app/
    Type=simple
    User=root
    ExecStart=/usr/bin/python3 /opt/dev/OwnGPT/app/app.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
    ***Make sure to adjust the path for "WorkingDirectory" and "ExecStart" accordingly to the path of the WAssist location***

    Next, run the following command to enable and start the service:
    ```bash
    systemctl enable assist. service
    systemctl start wassist.service
    ```
    To check the status of the service, run the following command:
    ```bash
    systemctl status wassist.servies
    ```

5. Expose the docker/service ports to the internet so WhatsApp servers can send the messages to your webhooks. this can be done using reverse proxy like **[Nginx](https://www.nginx.com/)**, **[Traefik](https://traefik.io/)** or **[Cloudflare Tunnel](https://www.cloudflare.com/products/tunnel/)**. Without this, you will not be able to communicate with the bot.



# Acknowledgments
Huge credit and a special thanks to [@mangate](https://github.com/mangate) for creating [SelfGPT](https://github.com/mangate/SelfGPT) which my code 
is based on.