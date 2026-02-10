from pydantic import BaseModel


class FileUploadRequest(BaseModel):
    filename: str
    content_type: str
    size: int


class FileUploadResponse(BaseModel):
    file_id: str
    upload_url: str
