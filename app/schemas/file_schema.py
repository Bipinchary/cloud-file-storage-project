from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID

class FileUploadRequest(BaseModel):
    filename: str
    content_type: str
    size: int


class FileUploadResponse(BaseModel):
    file_id: str
    upload_url: str

class FileResponse(BaseModel):
    id: UUID
    original_filename: str
    content_type: str
    size: int
    created_at: datetime

    class Config:
        from_attributes = True