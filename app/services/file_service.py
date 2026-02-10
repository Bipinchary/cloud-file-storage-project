import uuid
from sqlalchemy.orm import Session

from app.models import File
from app.core.aws import generate_presigned_upload_url
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
