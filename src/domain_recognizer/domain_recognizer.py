from dotenv import load_dotenv
import os
import openai
load_dotenv()
from langchain.chat_models import ChatOpenAI


from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.callbacks import get_openai_callback

from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.schema import SystemMessage

from src.domain_recognizer.prompts import recognition_prompt
from langchain.output_parsers import CommaSeparatedListOutputParser

from src.logger import logging

import re

class DomainRecognizer:

    def __init__(self, user_settings:dict):
        self.connect_to_llm(user_settings["openAI_model_name"])
        self._initialize_recognition_chain()

    def connect_to_llm(self, model_name:str):

        logging.info("Establishing connection to open ai models for domain recognition")
        try:
            self._llm = ChatOpenAI(model_name=model_name, temperature=0)

            messages = [
                        SystemMessage(
                                content="You are a helpful assistant that is able to recognize the domain of a company given it's name and a list of domains"
                        )
                        ]
            self._llm(messages)

        except Exception as excep:
            logging.error(f"Error establishing connection to llm for domain recognition: {excep}")

    def _initialize_recognition_chain(self):
        logging.info("Initializing domain recognition chain")
        try:
            output_parser = CommaSeparatedListOutputParser()        
            self._chain = LLMChain(llm=self._llm, prompt=recognition_prompt, output_key = "final_result", output_parser=output_parser, verbose=False)
        except Exception as excep:
            logging.error(f"Error initializing recognition chain: {excep}")


    def recognize_company_domain(self, company_name, domains: list):
        logging.info("Recognizing domains")
        try:
            if len(domains) == 0:
                return []
            
            str_domains = "\n".join(domains)

            filtered_result = self._chain({"text":str_domains, "company" : company_name})
            
            return filtered_result["final_result"][0]

        except Exception as excep:
            logging.error(f"Error while translating emails: {excep}")




       


