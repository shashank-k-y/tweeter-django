import boto3
from django.conf import settings

client = boto3.client(
    service_name='s3',
    region_name=settings.AWS_S3_REGION_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def get_presignedurl(key, content_type):
    params = {"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": key}
    if content_type:
        params.update(ResponseContentType=content_type)

    signed_url = client.generate_presigned_url(
        "get_object",
        Params=params,
    )
    return signed_url
