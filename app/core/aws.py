


import boto3
from botocore.config import Config
from app.core.config import settings

# Advanced configuration to prevent Signature and Redirection errors
s3_config = Config(
    region_name=settings.AWS_REGION,
    signature_version='s3v4',
    retries={'max_attempts': 3},
    s3={'addressing_style': 'virtual'}  # Ensures regional URL format
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    config=s3_config
)
'''s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)'''


''' def generate_presigned_upload_url(
    *, bucket: str, key: str, content_type: str, expires_in: int = 300
) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": bucket,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=expires_in,
    )


def generate_presigned_download_url(
    *, bucket: str, key: str, expires_in: int = 300
) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=expires_in,
    ) '''

def generate_presigned_upload_url(
    *, bucket: str, key: str, content_type: str, expires_in: int = 900
) -> str:
    """Generates a URL to UPLOAD a file directly to S3."""
    return s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": bucket,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=expires_in,
    )

def generate_presigned_download_url(
    *, bucket: str, key: str, expires_in: int = 3600
) -> str:
    """Generates a URL to DOWNLOAD/VIEW a file."""
    return s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": bucket,
            "Key": key,
        },
        ExpiresIn=expires_in,
    )
