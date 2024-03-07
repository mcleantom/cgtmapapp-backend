from uuid import uuid4

import boto3
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import ImageRouterConfig


def upload_image_to_s3(file: UploadFile, bucket_name: str, cloudfront: str) -> str:
    s3 = boto3.client("s3")
    filename = f"{uuid4()}{file.filename}"
    s3_key = f"images/{filename}"
    try:
        file.file.read()
        file.file.seek(0)
        s3.upload_fileobj(file.file, bucket_name, s3_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not upload file.") from e
    s3.generate_presigned_url("get_object", Params={"Bucket": bucket_name, "Key": s3_key})
    cloudfront_url = f"{cloudfront}/{s3_key}"
    return cloudfront_url


def create_images_router(config: ImageRouterConfig) -> APIRouter:
    router = APIRouter()

    @router.post("")
    def post_upload_file(file: UploadFile = File(...)) -> str:
        s3_url = upload_image_to_s3(file, config.bucket_name, config.cloudfront_url)
        return s3_url

    return router
