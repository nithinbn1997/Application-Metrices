import uuid

from fastapi import UploadFile, HTTPException

from app.config import attachment_table_name
from app.managers.doc_db_manager import doc_db_manager
from app.logger import get_logger


log = get_logger()

async def save_file(file_obj : UploadFile) -> str:
    """
    Save file object to DB, generate and return attachment id

    Args:
        file_obj (UploadFile): File object of the file to be uploaded
    """    
    attachment_id = str(uuid.uuid4())
    attachment_data = {
        "file_obj" : file_obj.file.read(),
        "attachment_id" : attachment_id
    }
    try: 
        doc_db_manager.add_document(attachment_table_name, attachment_data)
        data = await doc_db_manager.get_document_by_filter(attachment_table_name, {"attachment_id" : attachment_id})
        log.debug(f"added data -> {data}")
        return attachment_id
    except Exception as ex:
        log.error(f"Error saving file to DB -> {ex}")
        raise HTTPException(
            status_code = 503,
            detail = "Failed to upload file. Please try again later."
        )
