from fastapi import APIRouter, UploadFile, status, Response


from app import logger
from app.actions import upload_file_actions


log = logger.get_logger()

router = APIRouter(
    prefix="/api/v1/attachments",
    tags=["QCL Attachment APIs"],
)


@router.post("/upload")
async def upload_attachment(file: UploadFile):
    """
    Uploads attachment to Lattice system.
    Will be used for uploading LOA for now.

    Args:
        file (UploadFile): _description_

    Returns:
        dict: dictionary with attachment id
    """
    # Save the uploaded file to a temporary directory
    log.info("File upload API called")
    log.info("Saving file to DB")
    try:
        content_type: str = file.content_type
        file_extension: str = file.filename.rsplit(".")[1].lower()
        
        if (content_type != "application/pdf" or file_extension != "pdf"):
            return Response(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                content= "Invalid Media Format"
            )
        
        # Get the file size (in bytes)
        file.file.seek(0, 2)
        file_size = file.file.tell()

        # move the cursor back to the beginning
        await file.seek(0)

        if file_size > 10 * 1024 * 1024:
            # more than 10 MB
            return Response(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content= "File too large"
            )
    
        attachment_id = await upload_file_actions.save_file(file)
        log.info("Successfully uploaded file")
        log.debug(f"Saved file. Attachment ID: {attachment_id}")
        return {"attachment_id": attachment_id}
    except Exception as ex:
        log.exception(f"Failed to upload file. Error: {ex}")
