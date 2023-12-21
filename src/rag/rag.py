from src.logger import logging
from src.rag.rag_ingestor import DataIngestor
from src.rag.rag_engine import QueryEngineRAG
from src.rag.keyword_enhancer import KeywordEnhancer
from src.rag.prompts_query import query_prompt

from langchain.callbacks import get_openai_callback
from langchain.chains import LLMChain

class RAG:
    """
    Manager class to ingest data into the vector database and prompt the LLM. It also refines the prompts
    """

    def __init__(self, setup_dict):
        self._intialize_data_ingestor(setup_dict)
        self._initialize_query_engine(setup_dict)
        self._intialize_keyword_enhancer(setup_dict)

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

    def _intialize_keyword_enhancer(self, setup_dict):
        """
        establishes connection to a keyword_enhancer to shape questions
        """
        logging.info("Establishing connection to keyword enhancer")
        self._enhancer = KeywordEnhancer(setup_dict)

    def ingest_data_into_db(self, text:str, company_name:str, keywords: list):
        """
        saves the scraped data into the vector database
        Args:
            text (str): string representing the scraped text from internet
        """

        return self._ingestor.add(text, company_name, keywords)

    def prompt_engine(self, refined_prompts:list, keywords:list):
        """
        outputs prompt results for different prompts given by the user
        Args: 
            prompts (tuple(str,..)): a tuple of string of user prompts
        Returns:
            prompt_results (List[str]): a list of string representing the prompt outputs from gpt
        """
        try:
            prompt_results = dict()
            for i, prompt in enumerate(refined_prompts):
                prompt_results[keywords[i]]= self._engine.query(prompt)
            return prompt_results
        except Exception as e:
            logging.error(f"Error while prompting the querying engine: {e}")

    def create_prompts_from_keywords(self, company_name, keywords):
        try:
            questions = []
            for keyword in keywords:
                questions.append(self._enhancer.enhance(company_name, keyword))
            return questions
        except Exception as e:
            logging.error(f"Error while creating questions: {e}")        

    def refine_prompts(self, company_name, prompts):
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
                messages = query_prompt.format(company_name = company_name, query = prompt)
                
                refined_prompts.append(messages)
            return refined_prompts
        except Exception as excep:
            logging.error(f"Error while refining the prompts with company name and query: {excep}")
