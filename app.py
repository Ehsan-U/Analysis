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
    "system_message": "You are an AI agent responsible for managing mining industry data"
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
    summary, ingestion_tokens = rag.ingest_data_into_db(data["text"], data["company"])
    
    #Refine the prompts so that the query can be answered for the particular company then prompt the prompt engine
    refined_prompts =  rag.refine_prompts(data["company"], data["prompts"])
    prompt_results = rag.prompt_engine(refined_prompts) 
    
    #Get all the domains that were found in the summarized text
    domains = get_domains(summary)
    return jsonify({"domains": domains, "summary": summary, 'refined_prompts': refined_prompts, "prompt_results": prompt_results})


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
    company_name = data["company_name"]
    titles = data["prospects"]

    #
    if len(titles) == 0:
        return jsonify({"titles_converted": None})
    
    translated_titles = translator.translate(company_name, titles)

    return jsonify({"titles_converted": translated_titles})

@app.route('/filter_domains', methods=["POST"])
def process_domains():
    data = request.get_json()
    domains = data["domains"]
    company_name = data["company_name"]
    domain = domain_recognizer.recognize_company_domain(company_name, domains)

    return jsonify({company_name: domain})

@app.route('/prompt', methods=["POST"])
def process_query():
    data = request.get_json()
    

    return jsonify({"domain": "emails"})



if __name__ == '__main__':
    app.run(debug=True, port=5000)
