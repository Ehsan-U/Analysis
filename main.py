from fastapi import FastAPI


from src.email_processor.email_processor import EmailProcesssor
from src.logger import logging

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

setup_dict = {
    "openAI_model_name": "gpt-3.5-turbo-1106",
    "debug": True
}

logging.info("Initializing Email processor")
email_processor = EmailProcesssor(setup_dict)


@app.post('/find_email_pattern')
async def process_emails(data: dict):
    # Go through every domain in json and process its emails.
    response_data = {}
    for domain in data:
        response_data[domain] = await email_processor.process_emails(data[domain])

    return response_data
