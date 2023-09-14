from fastapi import APIRouter


from app import logger 
from app.managers.doc_db_manager import doc_db_manager
from app.config import transaction_table_name


log = logger.get_logger()

router = APIRouter(
    prefix="/db",
    tags=["DB_APIs"],
)


# @router.post("/create_collection")
# async def create_collection(collection_name : str):
#     """_summary_

#     Args:
#         collection_name (str): _description_
#     """    
#     await doc_db_manager.create_collection(collection_name)


@router.get("/list_collections")
async def list_collections():
    """_summary_

    Returns:
        _type_: _description_
    """    
    return await doc_db_manager.list_collections()

@router.get("/get_collection_data/")
async def get_collection_data(collection_name : str):
    """_summary_

    Args:
        collection_name (str): _description_

    Returns:
        _type_: _description_
    """    
    data = await doc_db_manager.get_all_documents(collection_name)
    return {
        "data" : data
    }

@router.get("/get_transaction_data")
async def get_transaction_data(transaction_id : str):
    """_summary_

    Args:
        transaction_id (str): _description_

    Returns:
        _type_: _description_
    """    
    log.debug(f"Received request to retrieve transaction data. ID -> {transaction_id}")
    filter_query = {"lattice_transaction_id" : transaction_id}
    return await doc_db_manager.get_document_by_filter(transaction_table_name, filter_query)
