from uuid import uuid4

import boto3
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from loguru import logger

from app.core.config import ImageRouterConfig


def upload_image_to_s3(file: UploadFile, bucket_name: str, cloudfront: str) -> str:
    s3 = boto3.resource(service_name="s3")
    filename = f"{uuid4()}{file.filename}"
    s3_key = f"images/{filename}"
    try:
        file.file.seek(0)
        s3.Bucket(bucket_name).upload_fileobj(
            Fileobj=file.file,
            Key=s3_key,
            ExtraArgs={"ContentType": file.content_type, "ACL": "public-read", "ContentEncoding": "base64"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not upload file.") from e
    return f"{cloudfront}/{s3_key}"


def create_images_router(config: ImageRouterConfig) -> APIRouter:
    router = APIRouter()

    @router.post("")
    def post_upload_file(request: Request, file: UploadFile = File(...)) -> str:
        logger.info(f"Uploading file {file.filename}")
        logger.info("Request headers: ", request.headers)
        logger.info("Request body: ", request.body)
        logger.info("Content type: ", file.content_type)
        s3_url = upload_image_to_s3(file, config.bucket_name, config.cloudfront_url)
        return s3_url

    return router
