import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID


from app.models import File , User
from app.models.file import FileStatus
from app.core.aws import (
    generate_presigned_upload_url,
    generate_presigned_download_url,
    s3_object_exists,
)
from app.core.config import settings




def create_file_upload(
    *,
    db: Session,
    owner_id: UUID,
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
        status=FileStatus.PENDING,
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



# CONFIRM UPLOAD (S3 HEAD CHECK)

def confirm_file_upload(
    *,
    db: Session,
    file_id: UUID,
    current_user: User,
):
    file = db.query(File).filter(File.id == file_id).first()

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    # Ownership check
    if file.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

    # Idempotent behavior
    if file.status == FileStatus.ACTIVE:
        return file

    exists = s3_object_exists(
        bucket=settings.AWS_S3_BUCKET,
        key=file.s3_key,
    )

    if not exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File not found in S3. Please ensure upload is complete.",
        )

    try:
        file.status = FileStatus.ACTIVE
        db.commit()
        db.refresh(file)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error during confirmation",
        )

    return file



#  LIST USER FILES


def list_user_files(
    *,
    db: Session,
    owner_id: UUID,
):
    return (
        db.query(File)
        .filter(
            File.owner_id == owner_id,
            File.is_deleted == False,
        )
        .order_by(File.created_at.desc())
        .all()
    )



#  DOWNLOAD (PRESIGNED GET)


def get_file_download_url(
    *,
    db: Session,
    file_id: UUID,
    requester_id: UUID,
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
        raise HTTPException(status_code=404, detail="File not found")

    # Ownership check (Phase 1 rule)
    if file.owner_id != requester_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if file.status != FileStatus.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail="File not available for download",
        )

    download_url = generate_presigned_download_url(
        bucket=settings.AWS_S3_BUCKET,
        key=file.s3_key,
    )

    return download_url
