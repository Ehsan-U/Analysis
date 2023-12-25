import pymongo

class MongoDBManager:
    def __init__(self, setup_dict):
        """
        Initializes the MongoDBManager with the provided setup dictionary.

        Args:
            setup_dict (dict): A dictionary containing MongoDB connection details.
                It should include the "connection_string" and "db_name" keys.

        Example:
            setup_dict = {
                "connection_string": "mongodb://localhost:27017/",
                "db_name": "my_database"
            }
            manager = MongoDBManager(setup_dict)
        """

        # MongoDB connection details
        self.client = pymongo.MongoClient(setup_dict["connection_string"])
        self._collection = None
        self._create_database(setup_dict["db_name"])

    def _create_database(self, database_name):
        """
        Creates or retrieves a reference to the specified database.

        Args:
            database_name (str): The name of the database to be created or retrieved.

        Example:
            manager = MongoDBManager(setup_dict)
            manager._create_database("my_database")
        """
        # Create or get a reference to the specified database
        self._database = self.client[database_name]
        print(f"Database '{database_name}' created or retrieved successfully.")

    def create_collection(self, collection_name):
        """
        Creates or retrieves a reference to the specified collection within the database.

        Args:
            collection_name (str): The name of the collection to be created or retrieved.

        Returns:
            pymongo.collection.Collection: The reference to the specified collection.

        Example:
            manager = MongoDBManager(setup_dict)
            collection = manager.create_collection("my_collection")
        """
        # Create or get a reference to the specified collection within the database
        collection = self._database[collection_name]
        print(f"Collection '{collection_name}' created or retrieved successfully.")
        return collection

    def upsert_data(self, company_name, data):
        """
        Upsert data into the specified collection for the given company name.

        Args:
            company_name (str): The name of the company for which data is to be upserted.
            data (dict): The data to be upserted into the collection.

        Returns:
            str: A success message indicating the upsert operation.

        Example:
            manager = MongoDBManager(setup_dict)
            manager.upsert_data("companyA", {"key": "value"})
        """

        
        #Define collection based on company name
        collection = self.create_collection(company_name)

        # Insert data into the specified collection
        data["_id"] = company_name
        data = {"$set": data}

        result = collection.update_one({"_id": company_name}, data, upsert=True)
        print(f"Inserted document ID: {result}")
        return "Success"

    def retrieve(self, company_name):
        """
        Retrieves a document from the specified collection based on the company name.

        Args:
            company_name (str): The name of the company for which data is to be retrieved.

        Returns:
            dict: The retrieved document.

        Example:
            manager = MongoDBManager(setup_dict)
            document = manager.retrieve("companyA")
        """
    
        collection = self.create_collection(company_name)
        return collection.find_one({"_id": company_name})

    def close_connection(self):
        """
        Closes the MongoDB connection.

        Example:
            manager = MongoDBManager(setup_dict)
            manager.close_connection()
        """

        # Close the MongoDB connection
        self.client.close()
        print("Connection closed.")