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

from src.email_processor.prompts import first_prompt, second_prompt, third_prompt
from langchain.output_parsers import CommaSeparatedListOutputParser

from src.logger import logging

import re

class EmailProcesssor:
    """
    This class processes emails using a chain of language models to identify and categorize patterns in the emails. It connects to a language model and defines a processing chain for analyzing email content.
    """
    def __init__(self, user_settings:dict):
        self.debug = user_settings["debug"]
        self.model_name = user_settings["openAI_model_name"]
        self._connect_to_llm(user_settings["openAI_model_name"])
        self._initialize_identification_chain()

    def _connect_to_llm(self, model_name:str):
        """
        establish connection to the llm
        """

        logging.info("Establishing connection to open ai models for email processing")
        try:
            self._llm = ChatOpenAI(model_name=model_name, temperature=0, max_tokens=4094)

            messages = [
                        SystemMessage(
                                content="You are a helpful assistant that specialize in identifying patterns in email addresses of a company. You are proficient in recognizing names in any language: European, American, British, Indian, Russian, Chinese, Middle Eastern, Pakistani, Japanese, Korean etc. You are able to expertly filter email addresses given a criteria"
                        )
                        ]
            self._llm(messages)

        except Exception as excep:
            logging.error(f"Error establishing connection to llm for email processing: {excep}")

    def _initialize_identification_chain(self):
        """
        Defines the identification chain, which is a sequence of LLMChains, each with a specific prompt and output key. This chain is responsible for processing emails and identifying patterns.

        The chain consists of three steps, each using a different prompt to guide the language model in processing and categorizing email content.
        """

        logging.info("Initializing email pattern recognition chains")
        try:
            self._chain_one = LLMChain(llm=self._llm, prompt=first_prompt, output_key="emails")
            self._chain_two = LLMChain(llm=self._llm, prompt=second_prompt, output_key="patterns")
            
            output_parser = CommaSeparatedListOutputParser()        
            self._chain_three = LLMChain(llm=self._llm, prompt=third_prompt, output_key = "final_result", output_parser=output_parser,verbose=False)
            
            # self.main_chain = SimpleSequentialChain(chains=[chain_one, chain_two, chain_three],
            #                                     verbose=True
            #                                     )
        except Exception as excep:
            logging.error(f"Error initializing chains: {excep}")

    def _post_process_text(self, patterns: str):
        """
        Post-processes the identified patterns to normalize and simplify the representation.

        Args:
            patterns (str): The string of patterns identified by the language model.

        Returns:
            str: A post-processed string where certain placeholders and formats have been standardized.
        """
        #return none if no patterns were found
        if patterns.strip().lower() == "none":
            return None

        patterns = patterns.strip().lower().split("@")[0].strip()
        
        patterns = patterns.replace("company domain", "")
        patterns = patterns.replace("companydomain", "")
        patterns = patterns.replace("dot", ".")
        patterns = patterns.replace("underscore", "_")
        patterns = patterns.replace("dash", "-")
        patterns = patterns.replace("hyphen", "-")
        patterns = patterns.replace("{", "[")
        patterns = patterns.replace("}", "]")
        patterns = patterns.replace("(", "[")
        patterns = patterns.replace(")", "]")
        
        patterns = patterns.replace("first name", "f")
        patterns = patterns.replace("last name", "l")
        patterns = patterns.replace("firstname", "f")
        patterns = patterns.replace("lastname", "l")
        patterns = patterns.replace("full first name", "f")
        patterns = patterns.replace("full last name", "l")
        patterns = patterns.replace("full firstname", "f")
        patterns = patterns.replace("full lastname", "l")
        patterns = patterns.replace("first name initial", "f1")
        patterns = patterns.replace("last name initial", "l1")
        patterns = patterns.replace("firstname initial", "f1")
        patterns = patterns.replace("lastname initial", "l1")
        patterns = patterns.replace("first initial", "f1")
        patterns = patterns.replace("last initial", "l1")
        patterns = patterns.replace("first letter of last name", "l1")
        patterns = patterns.replace("first letter of first name", "f1")
        patterns = patterns.replace("first letter of lastname", "l1")
        patterns = patterns.replace("first letter of firstname", "f1")
        patterns = patterns.replace("first initial of last name", "l1")
        patterns = patterns.replace("first initial of first name", "f1")
        patterns = patterns.replace("first initial of lastname", "l1")
        patterns = patterns.replace("first initial of firstname", "f1")
        patterns = patterns.replace("first", "f")
        patterns = patterns.replace("last", "l")
        patterns = patterns.replace("+", "")
        patterns = patterns.replace("[", "")
        patterns = patterns.replace("]", "")
        patterns = patterns.replace(" ", "")
        patterns = patterns.replace(",", ".")

        if len(patterns) > 5:
            return None
        
        return patterns

    async def process_emails(self, emails: list):
        """
        Processes a list of emails to identify patterns using the defined identification chain.

        Args:
            emails (list): A list of email strings to be processed.

        Returns:
            str or None: The identified patterns in a post-processed format, or None if no patterns are identified.
        """
        logging.info("Finding patterns in emails")
        try:
            if len(emails) == 0:
                return None

            emails = "\n".join(emails)
            
            #Recieve output as comma seperated string.
            filtered_emails =  self._chain_one.run(emails)
            if filtered_emails.strip() == "NONE":
                return None
            
            pattern_description =  self._chain_two.run(filtered_emails)
            identified_pattern = pattern_description.split("Single most common pattern found:")[-1]
            if pattern_description.strip() == "NONE":
                return None
            
            patterns =  self._chain_three.run({"structure": identified_pattern,  "emails": filtered_emails})

            #take the first pattern only
            patterns = patterns[0]   
            
            return self._post_process_text(patterns)
        except Exception as excep:
            logging.error(f"Error while processing emails: {excep}")




       


