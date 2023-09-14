import os
import json
from dotenv import load_dotenv

from pymongo import MongoClient
from pymongo.errors import OperationFailure
from bson import json_util

from app.logger import get_logger

log = get_logger()
load_dotenv()

class DocumentDB_Manager:

    def __init__(self) -> None:

        self.db_name = os.getenv("DB_NAME")
        try:
            self.doc_db_client = MongoClient(os.getenv("MONGO_URI"))
            log.debug("Connection to DocumentDB was successful.")
        except Exception as e:
            log.exception(f"Failed to connect to DocumentDB {e}" )

    async def close_connection(self):
        '''
        This function terminates document db connection.
        '''
        try:
            self.doc_db_client.close()
            log.debug("Successfully closed DocumentDB connection")
        except Exception as e:
            log.error(f"Failed to close DocumentDB connection. Error: {e}")

        
    async def list_collections(self):
        """
        List all collections within the specified database.

        Args:
            db_name (str): The name of the database to list collections from.

        Returns:
            list: A list of collection names within the specified database.

        Raises:
            OperationFailure: If listing collections fails.
        """
        try:
            db = self.doc_db_client[self.db_name]
            return db.list_collection_names()
        except OperationFailure as e:
            raise OperationFailure(f"Failed to list collections in database '{self.db_name}': {e}")


    async def create_collection(self, collection_name):
        """
        Create a new collection inside the specified database.

        Args:
            db_name (str): The name of the database containing the collection.
            collection_name (str): The name of the collection to create.

        Raises:
            OperationFailure: If the collection creation fails.
        """
        try:
            db = self.doc_db_client[self.db_name]
            var = db[collection_name]
        except OperationFailure as e:
            raise OperationFailure(f"Failed to create collection '{collection_name}' in database '{self.db_name}': {e}")

    async def get_all_documents(self, collection_name):
        """
        Get all documents from the specified collection.

        Args:
            db_name (str): The name of the database containing the collection.
            collection_name (str): The name of the collection to fetch documents from.

        Returns:
            list: A list of documents (dictionaries) present in the specified collection.

        Raises:
            OperationFailure: If fetching documents fails.
        """
        try:
            db = self.doc_db_client[self.db_name]
            collection = db[collection_name]
            data = collection.find()
            data = await self.parse_json(data)
             # log.debug(f"data -->>>> {data}")
            return list(data)
        except OperationFailure as e:
            raise OperationFailure(f"Failed to fetch documents from collection '{collection_name}' in database '{self.db_name}': {e}")


    async def parse_json(self, data):
        return json.loads(json_util.dumps(data))
           

    
    def add_document(self, collection_name, document):
        """
        Add a new document to the specified collection.

        Args:
            db_name (str): The name of the database containing the collection.
            collection_name (str): The name of the collection to add the document.
            document (dict): The document to be inserted.

        Raises:
            OperationFailure: If the document insertion fails.
        """
        try:
            db = self.doc_db_client[self.db_name]
            collection = db[collection_name]
            collection.insert_one(document)
            log.debug("Added document successfully.")
        except OperationFailure as e:
            raise OperationFailure(f"Failed to add document to collection '{collection_name}' in database '{self.db_name}': {e}")

    async def get_document_by_filter(self, collection_name, filter_query):
        """
        Get a specific document from the specified collection based on the filter query.

        Args:
            db_name (str): The name of the database containing the collection.
            collection_name (str): The name of the collection to fetch the document from.
            filter_query (dict): The query used to filter the document.

        Returns:
            dict: The document matching the filter query, or None if not found.

        Raises:
            OperationFailure: If fetching the document fails.
        """
        log.debug(f"Filter Query: {filter_query}")
        try:
            db = self.doc_db_client[self.db_name]
            collection = db[collection_name]
            data = collection.find_one(filter_query)
            data = await self.parse_json(data)
            return data
        except OperationFailure as e:
            raise OperationFailure(f"Failed to fetch document from collection '{collection_name}' in database '{self.db_name}': {e}")


    async def get_all_document_by_filter(self, collection_name, filter_query):
        """
        Get a specific document from the specified collection based on the filter query.

        Args:
            db_name (str): The name of the database containing the collection.
            collection_name (str): The name of the collection to fetch the document from.
            filter_query (dict): The query used to filter the document.

        Returns:
            dict: The document matching the filter query, or None if not found.

        Raises:
            OperationFailure: If fetching the document fails.
        """
        log.debug(f"Filter Query: {filter_query}")
        try:
            db = self.doc_db_client[self.db_name]
            collection = db[collection_name]
            return list(collection.find(filter_query))
        except OperationFailure as e:
            raise OperationFailure(f"Failed to fetch document from collection '{collection_name}' in database '{self.db_name}': {e}")
        
    async def get_attachment(self, collection_name, filter_query):
        """
        Get a specific document from the specified collection based on the filter query.

        Args:
            db_name (str): The name of the database containing the collection.
            collection_name (str): The name of the collection to fetch the document from.
            filter_query (dict): The query used to filter the document.

        Returns:
            dict: The document matching the filter query, or None if not found.

        Raises:
            OperationFailure: If fetching the document fails.
        """
        log.debug(f"Filter Query: {filter_query}")
        try:
            db = self.doc_db_client[self.db_name]
            collection = db[collection_name]
            return collection.find_one(filter_query)
        except OperationFailure as e:
            raise OperationFailure(f"Failed to fetch document from collection '{collection_name}' in database '{self.db_name}': {e}")

    
    async def delete_document(self, collection_name, filter_query):
        """
        Delete a document from the specified collection based on the filter query.

        Args:
            collection_name (str): The name of the collection from which to delete the document.
            filter_query (dict): The query used to filter the document to be deleted.

        Raises:
            OperationFailure: If the document deletion fails.
        """
        try:
            db = self.doc_db_client[self.db_name]
            collection = db[collection_name]
            collection.delete_one(filter_query)
        except OperationFailure as e:
            raise OperationFailure(f"Failed to delete document from collection '{collection_name}' in database '{self.db_name}': {e}")

    async def update_document(self, collection_name, filter_query, update_query):
        """
        Update a document in the specified collection based on the filter query.

        Args:
            db_name (str): The name of the database containing the collection.
            collection_name (str): The name of the collection in which to update the document.
            filter_query (dict): The query used to filter the document to be updated.
            update_query (dict): The update operation to be applied to the document.

        Raises:
            OperationFailure: If the document update fails.
        """
        try:
            db = self.doc_db_client[self.db_name]
            collection = db[collection_name]
            # log.debug(filter_query)
            # log.debug(update_query)
            collection.update_one(filter_query, update_query)
        except OperationFailure as e:
            raise OperationFailure(f"Failed to update document in collection '{collection_name}' in database '{self.db_name}': {e}")


doc_db_manager = DocumentDB_Manager()
