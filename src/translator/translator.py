from dotenv import load_dotenv
import os
import openai
load_dotenv()
from langchain.chat_models import ChatOpenAI
from src.utils import isCharacterPresent


from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.callbacks import get_openai_callback

from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.schema import SystemMessage

from src.translator.prompts import translation_prompt
from langchain.output_parsers import CommaSeparatedListOutputParser

from src.logger import logging

import re

class Translator:
    """
    This class processes emails using a chain of language models to identify and categorize patterns in the emails. 
    It connects to a language model and defines a processing chain for analyzing email content.
    """
    def __init__(self, user_settings:dict):
        """
        Initializes the Translator object.

        Parameters:
            user_settings (dict): A dictionary containing user settings, including the OpenAI model name.
        """
        self.connect_to_llm(user_settings["openAI_model_name"])
        self._initialize_translation_chain()

    def connect_to_llm(self, model_name:str):
        """
        Establishes a connection to OpenAI models for translation.

        Parameters:
            model_name (str): The name of the OpenAI language model to be used.
        """

        logging.info("Establishing connection to open ai models for translation")
        try:
            self._llm = ChatOpenAI(model_name=model_name, temperature=0)

            messages = [
                        SystemMessage(
                                content="You are a helpful assistant that is able to convert text from any language to English."
                        )
                        ]
            self._llm(messages)

        except Exception as excep:
            logging.error(f"Error establishing connection to llm for translation: {excep}")

    def _initialize_translation_chain(self):
        """
        Initializes the translation chain using the OpenAI language model.
        """
        logging.info("Initializing translation chain")
        try:

            output_parser = CommaSeparatedListOutputParser()        
            self._chain = LLMChain(llm=self._llm, prompt=translation_prompt, output_key = "final_result", output_parser=output_parser, verbose=True)
        
        except Exception as excep:
            logging.error(f"Error initializing translation chain: {excep}")

    def _mark_titles(self, titles: list):
        """
        Marks the indexes of non-empty titles in the input list.

        Parameters:
            titles (list): The list of titles to be marked.

        Returns:
            list: The list of marked indexes.
        """
        marked_places = [i for i in range(len(titles)) if (len(titles[i].strip("\n").strip()) > 0) and (isCharacterPresent(titles[i].strip("\n").strip()))]
        return marked_places

    def _preprocess_titles(self, titles: list):
        """
        Preprocesses the input list of titles by removing empty strings and leading/trailing whitespaces.

        Parameters:
            titles (list): The list of titles to be preprocessed.

        Returns:
            list: The preprocessed list of titles.
        """
        logging.info("Preprocessing titles")
        try:
            processed_titles = []
            for i in range(len(titles)):
                cleaned_title = titles[i].strip("\n").strip()
                if (len(cleaned_title) > 0):
                    if isCharacterPresent(cleaned_title):
                        processed_titles.append(cleaned_title)
                    else:
                        processed_titles.append("")
            return processed_titles
        except Exception as excep:
            logging.error("Error preprocessing titles {excep}")

        return []
    
    def _postprocess_titles(self, titles, translated_titles, marked_indexes):
        """
        Replaces the non-empty titles in the original list with their translated counterparts.

        Parameters:
            titles (list): The original list of titles.
            translated_titles (list): The list of translated titles.
            marked_indexes (list): The list of marked indexes.

        Returns:
            list: The updated list of titles with translated information.
        """
        try:
            for i, number in enumerate(marked_indexes):
                titles[number] = translated_titles[i]
        except Exception as excep:
            logging.error(f"Error translated titles inplace of original titles {excep}")
        
        return titles

    async def translate(self, company_name: str, titles: list):
        """
        Translates the titles of a company from their original language to English.

        Parameters:
            company_name (str): The name of the company.
            titles (list): The list of titles to be translated.

        Returns:
            list: The translated list of titles.
        """

        logging.info("Translating titles")
        try:
            #Store the indexes that has actual words in their position
            marked_indexes = self._mark_titles(titles)

            #Process all original list and remove empty spaces
            processed_titles = self._preprocess_titles(titles)
            if len(processed_titles) == 0:
                return titles

            #convert the list of titles into string and send to translation chain
            str_titles = "\n".join(processed_titles)
            translated_titles =  self._chain.run({"text":str_titles, "company": company_name})

            #Add the processed titles to the original list and return the translated information
            return self._postprocess_titles(titles, translated_titles, marked_indexes)

        except Exception as excep:
            logging.error(f"Error while translating emails: {excep}")
            return titles





       


