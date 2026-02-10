from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.auth import get_current_user
from app.models import User
from app.schemas.file_schema import FileUploadRequest, FileUploadResponse
from app.services.file_service import create_file_upload

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/upload-url", response_model=FileUploadResponse)
def get_upload_url(
    payload: FileUploadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    file, upload_url = create_file_upload(
        db=db,
        owner_id=current_user.id,
        filename=payload.filename,
        content_type=payload.content_type,
        size=payload.size,
    )

    return {
        "file_id": str(file.id),
        "upload_url": upload_url,
    }
