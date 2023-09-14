import uuid


from app.managers.doc_db_manager import doc_db_manager
from app.config import transaction_table_name
from app.logger import get_logger

log = get_logger()


class Transaction_Manager:
    def generate_lattice_transaaction_id(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return str(uuid.uuid4())

    def add_new_transaction_data(self, data):
        """_summary_

        Args:
            data (_type_): _description_
        """
        doc_db_manager.add_document(transaction_table_name, data)

    async def update_transaction_status(
        self, lattice_transaction_id: str, transaction_state: int
    ):
        """_summary_

        Args:
            lattice_transaction_id (str): _description_
            transaction_state (int): _description_
        """
        collection_name = transaction_table_name
        filter_query = {"lattice_transaction_id": lattice_transaction_id}
        update_query = {
            "$set": {
                "qcl_transaction_state": transaction_state
                }
        }
        await doc_db_manager.update_document(
            collection_name, filter_query, update_query
        )

    async def update_transaction_item_state(
        self, lattice_transaction_id: str, qcl_inventory_item_id: str, state: int
    ):
        """
        Update the state of the item in the transaction

        Args:
            lattice_transaction_id (str): lattice transaction id
            qcl_inventory_item_id (str): inventory item id of the item to be updated
            state (int): new state of the item
        """
        filter_query = {"lattice_transaction_id": lattice_transaction_id}
        trans_data = await doc_db_manager.get_document_by_filter(
            transaction_table_name, filter_query
        )
        log.debug(trans_data)

        trans_data = await doc_db_manager.get_document_by_filter(
            transaction_table_name, filter_query
        )
        items_data = trans_data.get("north_transaction_details_qcl_formatted")
        for i, item in enumerate(items_data):
            if item.get("qcl_inventory_item_id") == qcl_inventory_item_id:
                update_query = {
                    "$set": {
                        f"north_transaction_details_qcl_formatted.{i}.qcl_item_state": state
                    }
                }
            await doc_db_manager.update_document(
                transaction_table_name, filter_query, update_query
            )
            break

    async def get_all_transactions(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return await doc_db_manager.get_all_documents(transaction_table_name)

    async def update_north_update_state(self, transaction_id, state):
        """_summary_

        Args:
            transaction_id (_type_): _description_
            state (_type_): _description_
        """
        collection_name = transaction_table_name
        filter_query = {"lattice_transaction_id": transaction_id}
        update_query = {"$set": {"needs_north_update": state}}
        await doc_db_manager.update_document(
            collection_name, filter_query, update_query
        )


transaction_manager = Transaction_Manager()
