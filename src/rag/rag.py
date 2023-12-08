from src.logger import logging
from src.rag.rag_ingestor import DataIngestor
from src.rag.rag_engine import QueryEngineRAG
from src.rag.prompts import query_prompt

from langchain.callbacks import get_openai_callback

class RAG:
    """
    Manager class to ingest data into the vector database and prompt the LLM. It also refines the prompts
    """

    def __init__(self, setup_dict):
        self._intialize_data_ingestor(setup_dict)
        self._initialize_query_engine(setup_dict)


    def _initialize_query_engine(self, setup_dict):
        """
        establishes connection to vector database through query engine to prompt the database
        """
        logging.info("Establishing connection to Query Engine")
        self._engine = QueryEngineRAG(setup_dict)

    def _intialize_data_ingestor(self, setup_dict):
        """
        establishes connection to a vector database for uploaded data to it
        """
        logging.info("Establishing connection to Data Ingestor")
        self._ingestor = DataIngestor(setup_dict)

    def ingest_data_into_db(self, text:str, company:str):
        """
        saves the scraped data into the vector database
        Args:
            text (str): string representing the scraped text from internet
        """

        return self._ingestor.add(text, company)

    def prompt_engine(self, prompts:tuple):
        """
        outputs prompt results for different prompts given by the user
        Args: 
            prompts (tuple(str,..)): a tuple of string of user prompts
        Returns:
            prompt_results (List[str]): a list of string representing the prompt outputs from gpt
        """
        try:
            prompt_results = []
            for prompt in prompts:
                prompt_results.append(self._engine.query(prompt))
            return prompt_results
        except Exception as e:
            logging.error(f"Error while prompting the querying engine: {e}")

    def refine_prompts(self, company, prompts):
        """
        Outputs prompt results for different prompts given by the user
        Args: 
            prompts (tuple(str,..)): a tuple of string of user prompts
        Returns:
            prompt_results (List[str]): a list of string representing the prompt outputs from gpt
        """
        
        try:
            refined_prompts = []
            for prompt in prompts:
                
                messages = query_prompt.format(company = company, query = prompt)
                
                refined_prompts.append(messages)
            return refined_prompts
        except Exception as excep:
            logging.error(f"Error while refining the prompts with company name and query: {excep}")
