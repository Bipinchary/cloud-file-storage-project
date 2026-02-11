import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.models.file import File, FileStatus
from app.core.config import settings
from app.core.aws import (
    generate_presigned_upload_url,
    generate_presigned_download_url,
    s3_object_exists
)

def create_file_upload(*, db: Session, owner_id: uuid.UUID, filename: str, content_type: str, size: int):
    file_id = uuid.uuid4()
    # Organized S3 Path: users/UUID/file_UUID/filename
    s3_key = f"users/{owner_id}/{file_id}/{filename}"

    file = File(
        id=file_id,
        owner_id=owner_id,
        s3_key=s3_key,
        original_filename=filename,
        content_type=content_type,
        size=size,
        status=FileStatus.PENDING # Always start as pending
    )

    db.add(file)
    db.commit()
    db.refresh(file)

    upload_url = generate_presigned_upload_url(
        bucket=settings.AWS_S3_BUCKET,
        key=s3_key,
        content_type=content_type
    )

    return file, upload_url

def confirm_file_upload(*, db: Session, file: File, current_user_id: uuid.UUID):
    # Security Check
    if file.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this file")

    # Idempotency: If already active, just return
    if file.status == FileStatus.ACTIVE:
        return file

    # Verify physical existence in S3
    exists = s3_object_exists(bucket=settings.AWS_S3_BUCKET, key=file.s3_key)

    if not exists:
        file.status = FileStatus.FAILED
        db.commit()
        raise HTTPException(status_code=400, detail="File was not found in S3 storage")

    file.status = FileStatus.ACTIVE
    db.commit()
    db.refresh(file)
    return file

def get_file_download_url(*, db: Session, file_id: uuid.UUID, requester_id: uuid.UUID):
    file = db.query(File).filter(File.id == file_id, File.is_deleted == False).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if file.owner_id != requester_id:
        raise HTTPException(status_code=403, detail="Access denied")

    if file.status != FileStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="File is not ready for download. Please confirm upload first.")

    return generate_presigned_download_url(bucket=settings.AWS_S3_BUCKET, key=file.s3_key)

def list_user_files(*, db: Session, owner_id: uuid.UUID) -> List[File]:
    return db.query(File).filter(
        File.owner_id == owner_id, 
        File.is_deleted == False
    ).order_by(File.created_at.desc()).all()