from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
load_dotenv()

from src.summarizer.summarization_tool import Summarizer
from src.email_processor.email_processor import EmailProcesssor
from src.translator.translator import Translator
from src.domain_recognizer.domain_recognizer import DomainRecognizer
from src.logger import logging
from src.utils import extract_information
import uvicorn
import os


app = FastAPI()

setup_dict = {
    "openAI_model_name": "gpt-3.5-turbo-1106",
    "debug": True
}

logging.info("Initializing summarization engine")
summarizer = Summarizer(setup_dict)

logging.info("Initializing Email processor")
email_processor = EmailProcesssor(setup_dict)

logging.info("Initializing Translator")
translator = Translator(setup_dict)

logging.info("Initializing Domain Recognizer")
domain_recognizer = DomainRecognizer(setup_dict)


@app.post('/analyze')
async def process_text(request_data: dict):
    # Summarize all the information in the scrapped data
    summary = await summarizer.process(request_data["text"], request_data['company'], request_data["keywords"])

    # Extract all information and make a dictionary with keywords as keys
    response_data = await extract_information(summary, request_data["keywords"])

    return response_data


@app.post('/find_email_pattern')
async def process_emails(data: dict):
    # Go through every domain in json and process its emails.
    response_data = {}
    for domain in data:
        response_data[domain] = await email_processor.process_emails(data[domain])

    return response_data


@app.post('/convert_titles')
async def process_titles(data: dict):
    response_data = {}
    # get company name and prospects list extracted
    for company_name, prospects in data.items():

        # Extract all the titles from prospects
        titles = [prospect["title"] for prospect in prospects]

        # if there are no titles available then just return the same information back
        if len(titles) == 0:
            response_data[company_name] = prospects
        else:
            # Translate the titles and return a list of translated titles
            translated_titles = await translator.translate(company_name, titles)

            # Replace the titles in those same positions
            for i, prospect in enumerate(prospects):
                prospect["title"] = translated_titles[i]

            response_data[company_name] = prospects

    return response_data


@app.post('/filter_domains')
async def process_domains(data: dict):
    # company name as key and list of domains as value
    domains = []
    for key, potential_domains in data.items():
        company_name = key

        # Recognize the company domain from potential domains
        domain = await domain_recognizer.recognize_company_domain(company_name, potential_domains)
        domains.append(domain)

    response_data = {key: domain for key, domain in zip(data.keys(), domains)}

    return response_data


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000)
