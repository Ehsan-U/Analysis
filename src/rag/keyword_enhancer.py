import os
import re
import openai
from src.logger import logging

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback

from src.rag.prompts_query import keyword_prompt

openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = os.getenv("CONNECTION_STRING_VECTOR_DB")

class KeywordEnhancer:
    """
    This class represents a Keyword based prompt enhance. It converts keywords into actual questions.
    """

    def __init__(self, user_settings:dict):
        """
        Initializes the KeywordEnhancer with user-defined settings.

        Args:
            user_settings (dict): A dictionary containing settings such as the OpenAI model name and collection name for the vector store.
        """
        self._connect_to_llm(user_settings["openAI_model_name"])
        self._initialize_enhancer()

    def _connect_to_llm(self, model_name:str):
        """
        Establishes a connection to the language model (LLM) provided by OpenAI.

        Args:
            model_name (str): The name of the OpenAI model to connect to.

        Logs an information message on successful connection and an error message if the connection fails.
        """

        logging.info("Establishing connection to open ai models for enhancing")
        try:
            self._llm = ChatOpenAI(model_name=model_name, temperature=0)
        except Exception as e:
            logging.error(f"Error establishing connection to open ai models for enhancing: {e}")

    def _initialize_enhancer(self):
        """
        Intialize the enhancer
        """
        logging.info("Intializing enhancer")
        try:
            self._chain = LLMChain(llm=self._llm, prompt=keyword_prompt, output_key = "result")
        except Exception as excep:
            logging.error(f"Error intializing keyword enhancer: {excep}")

    def enhance(self, company_name: str, keyword: str):
        
        logging.info("Enhancing the keywords")
        try:
            result = self._chain.run({"company_name":company_name, "keyword": keyword})
            return result
        except Exception as excep:
            logging.error(f"Error querying the query engine: {excep}")