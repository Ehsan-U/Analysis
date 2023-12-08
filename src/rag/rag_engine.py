import os
import openai
from dotenv import load_dotenv
from src.logger import logging
load_dotenv()

from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.vectorstores import PGVector

from langchain.chains import RetrievalQA

from langchain.chat_models import ChatOpenAI


openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = os.getenv("CONNECTION_STRING_VECTOR_DB")

class QueryEngineRAG:
    """
    This class represents a Query Engine using Retrieval-Augmented Generation (RAG). It manages connections to language models and vector stores for the purpose of executing complex queries that involve retrieving and generating information.
    """

    def __init__(self, user_settings:dict):
        """
        Initializes the QueryEngineRAG with user-defined settings.

        Args:
            user_settings (dict): A dictionary containing settings such as the OpenAI model name and collection name for the vector store.
        """
        self._connect_to_llm(user_settings["openAI_model_name"])
        self._connect_to_vector_store(CONNECTION_STRING, user_settings["collection_name"])
        self._initialize_the_query_engine()

    def _connect_to_llm(self, model_name:str):
        """
        Establishes a connection to the language model (LLM) provided by OpenAI.

        Args:
            model_name (str): The name of the OpenAI model to connect to.

        Logs an information message on successful connection and an error message if the connection fails.
        """

        logging.info("Establishing connection to open ai models for prompting")
        try:
            self._llm = ChatOpenAI(model_name=model_name, temperature=0)

            self._embedding_llm = OpenAIEmbeddings(
                                model="text-embedding-ada-002",
                            )
        except Exception as e:
            logging.error(f"Error establishing connection to open ai models for prompting: {e}")


    def _connect_to_vector_store(self, connection_string, collection_name):
        """
        Establishes a connection to the vector database using the given connection string and collection name. Also initializes the query engine.

        Args:
            connection_string (str): The connection string for the vector database.
            collection_name (str): The name of the collection within the vector database.

        Logs an error message if the connection to the vector database or the initialization of the query engine fails.
        """

        logging.info(f"Establishing connection to vector database for query engine")
        try:
            self._vector_store = PGVector(embedding_function=self._embedding_llm,
                                    collection_name=collection_name,
                                    connection_string=connection_string,
                                    )
        except Exception as e:
            logging.error(f"Error establishing connection to vector database for query engine {e}")

    def _initialize_the_query_engine(self):
        """
        Intializes the query engine
        """
        logging.info("Intializing query engine")
        try:
            self._query_engine = RetrievalQA.from_chain_type(llm=self._llm, chain_type="stuff", retriever=self._vector_store.as_retriever(search_kwargs={'k': 10, 'score_threshold': 5}))
        except Exception as excep:
            logging.error(f"Error intializing query engine: {excep}")

    def query(self, query_string: str):
        """
        Executes a query using the RetrievalQA query engine, leveraging both the language model and the vector store.

        Args:
            query_string (str): The query string to be processed.

        Returns:
            The result of the query.
        """
        try: 
            return self._query_engine.run(query_string)
        except Exception as excep:
            logging.error(f"Error querying the query engine: {excep}")
        