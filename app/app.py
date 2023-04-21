import os
import uvicorn
from pathlib import Path
from loguru import logger
from manish import MaNish
from fastapi import FastAPI, Request
from commandhandler import CommandHandler

app = FastAPI()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
manish = MaNish(os.getenv("TOKEN"), phone_number_id=os.getenv("PHONE_NUMBER_ID"))
ALLOWED_NUMBERS = os.getenv("ALLOWED_NUMBERS")
commandHandler = CommandHandler()
audio_dir = Path.cwd() / "audio/"
audio_dir.mkdir(parents=True, exist_ok=True)

@app.get("/", include_in_schema=False)
async def verify(request: Request):
    if request.query_params.get('hub.mode') == "subscribe" and request.query_params.get("hub.challenge"):
        if not request.query_params.get('hub.verify_token') == VERIFY_TOKEN: 
            return "Verification token mismatch", 403
        return int(request.query_params.get('hub.challenge'))
    return "Hello world", 200



@app.post("/", include_in_schema=False)
async def webhook(request: Request):
    data = await request.json()
    changed_field = manish.changed_field(data)
    if changed_field == "messages":
        new_message = manish.get_mobile(data)

        if new_message:
            mobile = manish.get_mobile(data)
            message_type = manish.get_message_type(data)
            message_id = manish.get_message_id(data)
            manish.set_status(message_id)
            if message_type == "text" and mobile in ALLOWED_NUMBERS:
                message = manish.get_message(data)
                result = commandHandler.execute_command(message)
                if result.lower().endswith(".png"):
                    manish.send_image(result, mobile)
                    os.remove(result)
                else:
                    manish.send_message(result, mobile)
            elif message_type == "audio":
                audio = manish.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = manish.query_media_url(audio_id)
                audio_filename = manish.download_media(audio_url, mime_type, audio_dir)
                result = commandHandler.transcript(audio_filename)
                manish.send_message(result, mobile)
            else:
                logger.info(f"{mobile} sent {message_type} ")
                logger.info(data)
        else:
            delivery = manish.get_delivery(data)
            if delivery:
                logger.info(f"Message : {delivery}")
            else:
                logger.info("No new message")
    return "ok"

if __name__ == '__main__':
    logger.info("Whatsapp Webhook is up and running")
    uvicorn.run(app, host="0.0.0.0", port=7020)