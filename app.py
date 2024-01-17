from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv() #call this before importing RAG class

from src.summarizer.summarization_tool import Summarizer

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
    "openAI_model_name": "gpt-3.5-turbo-1106",
     "debug" : True
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
    request_data = request.get_json()

    company_name = request_data['company']

    #Summarize all the information in the scrapped data
    summary = summarizer.process(request_data["text"], request_data['company'], [request_data["topic"]])

    #Extract all information and make a dictionary with keywords as keys
    response_data = extract_information(summary, [request_data["topic"]])
    response_data = {company_name: response_data}

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
    
    response_data = dict()
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
            response_data[company_name] = prospects
            
        #Translate the titles and return a list of translated titles
        translated_titles = translator.translate(company_name, titles)

        #Replace the titles in those same positions
        for i, prospect in enumerate(prospects):
            prospect["title"] =  translated_titles[i]

        response_data[company_name] = prospects

    return jsonify(response_data)

@app.route('/filter_domains', methods=["POST"])
def process_domains():
    data = request.get_json()
    
    #company name as key and list of domains as value
    domains = []
    for key in data:
        company_name = key
        domains = data[key]

        #Recognize the company domain from a potential domains
        domain = domain_recognizer.recognize_company_domain(company_name, domains)
        domains.append(domain)

    response_data = dict()
    for i, key in enumerate(data):
        response_data[key] = domains[i]
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
