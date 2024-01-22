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
    """
    A class for recognizing the domain of a company given its name and a list of domains.

    Attributes:
        _llm (ChatOpenAI): An instance of the ChatOpenAI class for language model interaction.
        _chain (LLMChain): An instance of the LLMChain class for processing and recognizing domains.

    Methods:
        __init__(self, user_settings: dict):
            Initializes the DomainRecognizer object by connecting to the OpenAI language model and
            initializing the domain recognition chain.

        connect_to_llm(self, model_name: str):
            Establishes a connection to OpenAI models for domain recognition.

        _initialize_recognition_chain(self):
            Initializes the domain recognition chain using the OpenAI language model.

        _preprocess_domains(self, domains: list) -> list:
            Preprocesses the input list of domains by removing empty strings and leading/trailing whitespaces.

        recognize_company_domain(self, company_name, domains: list) -> list:
            Recognizes the domain of a company given its name and a list of domains.

    """
    def __init__(self, user_settings:dict):
        """
        Initializes the DomainRecognizer object.

        Parameters:
            user_settings (dict): A dictionary containing user settings, including the OpenAI model name.
        """
        self.debug = user_settings["debug"]
        self.connect_to_llm(user_settings["openAI_model_name"])
        self._initialize_recognition_chain()

    def connect_to_llm(self, model_name:str):
        """
        Establishes a connection to OpenAI models for domain recognition.

        Parameters:
            model_name (str): The name of the OpenAI language model to be used.
        """

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
        """
        Initializes the domain recognition chain using the OpenAI language model.
        """
        logging.info("Initializing domain recognition chain")
        try:
            output_parser = CommaSeparatedListOutputParser()        
            self._chain = LLMChain(llm=self._llm, prompt=recognition_prompt, output_key = "final_result", output_parser=output_parser, verbose=False)
        except Exception as excep:
            logging.error(f"Error initializing recognition chain: {excep}")
    
    def _preprocess_domains(self, domains: list):
        """
        Preprocesses the input list of domains by removing empty strings and leading/trailing whitespaces.

        Parameters:
            domains (list): The list of domains to be preprocessed.

        Returns:
            list: The preprocessed list of domains.
        """
        processed_titles = [domains[i].strip() for i in range(len(domains)) if domains[i].strip() != ""]
        return processed_titles

    async def recognize_company_domain(self, company_name: str, domains: list):
        """
        Recognizes the domain of a company given its name and a list of domains.

        Parameters:
            company_name: The name of the company.
            domains (list): The list of domains associated with the company.

        Returns:
            list: The recognized domain(s) of the company.
        """
        logging.info("Recognizing domains")
        company_name = company_name[0]
        try:
            #Remove domains are empty spaces
            domains = self._preprocess_domains(domains)

            #If no domains are available then just return empty list
            if len(domains) == 0:
                return []
            
            #Convert domains into str and run the chain
            str_domains = "\n".join(domains)
            filtered_result = self._chain({"text":str_domains, "company" : company_name})
            
            #Filter and access the final output
            return filtered_result["final_result"][0]

        except Exception as excep:
            logging.error(f"Error while translating emails: {excep}")
        
        return []




       


