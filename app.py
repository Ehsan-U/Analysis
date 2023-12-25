from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv() #call this before importing RAG class

from src.summarizer.summarization_tool import Summarizer
from src.db_manager.mongo_db import MongoDBManager

from src.logger import logging
from langchain.callbacks import get_openai_callback
from src.utils import connect_to_token_df, get_domains

from src.email_processor.email_processor import EmailProcesssor
from src.translator.translator import Translator
from src.domain_recognizer.domain_recognizer import DomainRecognizer

from src.logger import logging
from src.utils import extract_information

import os

app = Flask(__name__)

setup_dict = {
    "connection_string" : os.environ["MONGO_CONNECTION_STRING"],
    "db_name": os.environ["db_name"],
    "collection_name": os.environ["collection_name"],
}

logging.info("Intializing database connection")
db = MongoDBManager(setup_dict)

setup_dict = {
    "openAI_model_name": "gpt-3.5-turbo-1106",
}

logging.info("Intializing summarization engine")
summarizer = Summarizer(setup_dict)

logging.info("Intializing Email processor")
email_processor = EmailProcesssor(setup_dict)

logging.info("Intializing Translator")
translator = Translator(setup_dict)

logging.info("Intializing Domain Recognizer")
domain_recognizer = DomainRecognizer(setup_dict)

@app.route('/analyze', methods=["POST"])
def process_text():
    data = request.get_json()

    #Summarize all the information in the scrapped data
    summary = summarizer.process(data["text"], data["company"], data["keywords"])

    #Extract all information and make a dictionary with keywords as keys
    response_data = extract_information(summary, data["keywords"])

    return jsonify(response_data)

@app.route('/store_in_db', methods=["POST"])
def ingest():
    data = request.get_json()

    #Ingest data into the database
    #data["summary"] is the <keyword>: <extracted information> pairs
    try:
        db.upsert_data(data["company"], data["summary"])
        response_data = {'message': 'Record created successfully'}
    except Exception as excep:
        logging.error(f"Error processing ingestion request, {excep}")
        response_data = {'message': 'Record creation was not successful'}

    return jsonify(response_data)

@app.route('/retrieve_from_db', methods=["POST"])
def retrieve():
    data = request.get_json()

    #retrieve a document through company name
    response_data = db.retrieve(data["company"])

    return jsonify(response_data)

@app.route('/find_email_pattern', methods=["POST"])
def process_emails():
    data = request.get_json()

    #Go through every domain in json and process its emails.
    response_data= dict()
    for domain in data: 
        response_data[domain] = email_processor.process_emails(data[domain])
    
    return jsonify(response_data)

@app.route('/convert_titles', methods=["POST"])
def process_titles():
    data = request.get_json()
    
    #get company name and prospects list extracted
    for key in data:
        company_name = key
        prospects = data[key]

    #Extract all the titles from prospects
    titles = []
    for prospect in prospects:
        titles.append(prospect["title"])

    # if there are no titles available then just return the same information back
    if len(titles) == 0:
        return jsonify({company_name: prospects})
    
    #Translate the titles and return a list of translated titles
    translated_titles = translator.translate(company_name, titles)

    #Replace the titles in those same positions
    for i, prospect in enumerate(prospects):
        prospect["title"] =  translated_titles[i]

    return jsonify({company_name: prospects})

@app.route('/filter_domains', methods=["POST"])
def process_domains():
    data = request.get_json()
    #company name as key and list of domains as value

    for key in data:
        company_name = key
        domains = data[key]

    #Recognize the company domain from a potential domains
    domain = domain_recognizer.recognize_company_domain(company_name, domains)

    return jsonify({company_name: domain})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
