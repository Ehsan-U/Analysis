from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv() #call this before importing RAG class

from src.rag.rag import RAG
from src.logger import logging
from langchain.callbacks import get_openai_callback
from src.utils import connect_to_token_df, get_domains

from src.email_processor.email_processor import EmailProcesssor
from src.translator.translator import Translator
from src.domain_recognizer.domain_recognizer import DomainRecognizer

from src.logger import logging


app = Flask(__name__)

setup_dict = {
    "collection_name": "ab_testing",
    "pre_delete_collection": True,
    "openAI_model_name": "gpt-3.5-turbo-1106",
}

logging.info("Intializing RAG engine")
rag = RAG(setup_dict)

logging.info("Intializing Email processor")
email_processor = EmailProcesssor(setup_dict)

logging.info("Intializing Translator")
translator = Translator(setup_dict)

logging.info("Intializing Translator")
domain_recognizer = DomainRecognizer(setup_dict)

@app.route('/analyze', methods=["POST"])
def process_text():
    data = request.get_json()

    #Ingest data into the vector database
    summary, ingestion_tokens = rag.ingest_data_into_db(data["text"], data["company"], data["keywords"])
    # print(summary)

    prompts = rag.create_prompts_from_keywords(data["company"], data["keywords"])

    #Refine the prompts so that the query can be answered for the particular company then prompt the prompt engine
    # refined_prompts =  rag.refine_prompts(data["company"], data["prompts"])
    refined_prompts = rag.refine_prompts(data["company"], prompts)
    prompt_results = rag.prompt_engine(refined_prompts, data["keywords"])

    return jsonify(prompt_results)

@app.route('/find_email_pattern', methods=["POST"])
def process_emails():
    data = request.get_json()

    #Go through every domain in json and process its emails.
    result= dict()
    for domain in data: 
        result[domain] =  email_processor.process_emails(data[domain])
    
    return jsonify(result)

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

@app.route('/prompt', methods=["POST"])
def process_prompt():
    data = request.get_json()
    
    for key in data:
        company_name = key
        prompts = data[key]
    
    #Refine the prompts to make some clarifications
    refined_prompts =  rag.refine_prompts(company_name, prompts)
    prompt_results = rag.prompt_engine(refined_prompts) 
    
    #Return output with company name and a list
    return jsonify({company_name: prompt_results})


if __name__ == '__main__':
    app.run( debug=True, port=5000)
