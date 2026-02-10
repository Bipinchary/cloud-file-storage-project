import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import File
from app.core.aws import (
    generate_presigned_upload_url,
    generate_presigned_download_url,
)
from app.core.config import settings


def create_file_upload(
    *,
    db: Session,
    owner_id,
    filename: str,
    content_type: str,
    size: int,
):
    file_id = uuid.uuid4()
    s3_key = f"users/{owner_id}/{file_id}/{filename}"

    file = File(
        id=file_id,
        owner_id=owner_id,
        s3_key=s3_key,
        original_filename=filename,
        content_type=content_type,
        size=size,
    )

    db.add(file)
    db.commit()
    db.refresh(file)

    upload_url = generate_presigned_upload_url(
        bucket=settings.AWS_S3_BUCKET,
        key=s3_key,
        content_type=content_type,
    )

    return file, upload_url


def list_user_files(*, db: Session, owner_id):
    return (
        db.query(File)
        .filter(
            File.owner_id == owner_id,
            File.is_deleted == False,
        )
        .order_by(File.created_at.desc())
        .all()
    )


def get_file_download_url(
    *,
    db: Session,
    file_id,
    requester_id,
):
    file = (
        db.query(File)
        .filter(
            File.id == file_id,
            File.is_deleted == False,
        )
        .first()
    )

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    if file.owner_id != requester_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this file",
        )

    download_url = generate_presigned_download_url(
        bucket=settings.AWS_S3_BUCKET,
        key=file.s3_key,
    )

    return download_url
