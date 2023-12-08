import os
import re
import openai
from src.logger import logging
from src.rag.prompts import map_prompt, reduce_prompt

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import PGVector
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback


openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = os.getenv("CONNECTION_STRING_VECTOR_DB")

class DataIngestor:
    """
    This is a data ingestor call that is responsible for preprocess, split and store data into the vector database
    """
    def __init__(self, user_settings:dict):
        """
        Initializes the DataIngestor with user settings.

        Args:
            user_settings (dict): A dictionary containing settings for the ingestor, such as the OpenAI model name and collection name for the vector store.
        """

        self._reduction_max_tokens = 4000
        self.connect_to_llm(user_settings["openAI_model_name"])
        self.connect_to_vector_store(CONNECTION_STRING, user_settings["collection_name"], user_settings["pre_delete_collection"])
        self.define_summary_text_splitter()
        self.define_db_text_splitter()
        self._initialize_summarizer()

    def connect_to_llm(self, model_name:str):
        """
        Establishes a connection to the language model (LLM).

        Args:
            model_name (str): The name of the OpenAI model to be used.
        """
        logging.info("Establishing connection to open ai models for data ingestor")
        try: 
            self._llm = ChatOpenAI(model_name= model_name, temperature=0)
            self._embedding_llm = OpenAIEmbeddings(
                            model="text-embedding-ada-002",
                        )
        except Exception as excep:
            logging.error(f"Error establishing connection to open ai models for ingestor: {excep}")


    def define_summary_text_splitter(self):
        """
        Defines text splitter for when we are splitting to store into the vector database
        """
        self._sum_text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                                chunk_size=8000, chunk_overlap=0.5
                            )
    
    def define_db_text_splitter(self):
        """
        Defines text splitter for when we are splitting to store into the vector database
        """
        self._db_text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                                chunk_size=1024, chunk_overlap=0.5
                            )

    def connect_to_vector_store(self, connection_string, collection_name, pre_delete_collection):
        """
        Establishes a connection to the vector database.

        Args:
            connection_string (str): The connection string for the vector database.
            collection_name (str): The name of the collection within the vector database.
        """

        logging.info("Establishing connection to pgvector vector store for data ingestor")
        self._vector_store = PGVector(embedding_function=self._embedding_llm,
                                collection_name=collection_name,
                                connection_string=connection_string,
                                pre_delete_collection = pre_delete_collection,
                                )


    def _text_preprocessor(self, text):
        """
        Preprocesses the given text by removing HTTP links, empty brackets, and normalizing spaces.

        Args:
            text (str): The text to preprocess.

        Returns:
            str: The cleaned and preprocessed text.
        """
        # Define a regular expression pattern to match HTTP links
        http_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        # Use re.sub to replace HTTP links with an empty string
        cleaned_text = re.sub(http_pattern, '', text)
        # Define a regular expression pattern to match empty square brackets
        empty_brackets_pattern = r'\[\s*\]'
        # Use re.sub to replace empty square brackets with an empty string
        cleaned_text = re.sub(empty_brackets_pattern, '', cleaned_text)
        # Define a regular expression pattern to match square brackets without alphabets
        no_alphabet_brackets_pattern = r'\[[^\w]*\]'
        # Use re.sub to replace square brackets without alphabets with an empty string
        cleaned_text = re.sub(no_alphabet_brackets_pattern, '', cleaned_text)
        # Use a regular expression to replace multiple spaces with a single space
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        # Use regular expression to replace consecutive "\n" with a single "\n"
        cleaned_text = re.sub(r'\n+', '\n', cleaned_text)

        return cleaned_text

    def _initialize_summarizer(self):
        """
        Initializes the summarization process by setting up various chains and reducers for document processing and summarization.
        """
        map_chain = LLMChain(llm=self._llm, prompt=map_prompt)

        # Run chain
        reduce_chain = LLMChain(llm=self._llm, prompt=reduce_prompt)

        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="docs"
        )

        # Combines and iteravely reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=self._reduction_max_tokens,
        )

        # Combining documents by mapping a chain over them, then combining results
        self._map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=map_chain,
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="docs",
            # Return the results of the map steps in the output
            return_intermediate_steps=False,
        )

    def _summarize(self, text, company):
        """
        Summarizes the given split documents for a specified company.

        Args:
            text: The document to summarize as string.
            company: The company name for which the summarization is being done as string.

        Returns:
            The summarized content.
        """

        split_documents = self._sum_text_splitter.create_documents([text])
        return self._map_reduce_chain.run(input_documents=split_documents, company = company)

    def add(self, text, company):
        """
        Preprocesses, summarizes, and adds the given text to the vector database.

        Args:
            text (str): The text content representing the scraped data.
            company: The company associated with the text.

        Returns:
            A tuple containing the summarized content and token consumption information.
        """

        text = self._text_preprocessor(text)

        with get_openai_callback() as cb: 
            logging.info("Summarizing the text for vector database")
            summarized_content = self._summarize(text, company)
            
            logging.info("Adding documents into the vector database")
            split_docs = self._db_text_splitter.create_documents([summarized_content])
            if len(split_docs) > 4:
                logging.warning(f"Too many chunks were made for summarization: {len(split_docs)}")
            self._vector_store.add_documents(split_docs)
            token_consumption = cb
        return summarized_content, token_consumption