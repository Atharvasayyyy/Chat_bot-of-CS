# services/storage_service.py
import boto3
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def upload_image(file, filename):
    try:
        bucket = os.getenv("AWS_BUCKET_NAME")

        s3.upload_fileobj(
            file,
            bucket,
            filename,
            ExtraArgs={"ContentType": "image/jpeg"}
        )

        return f"https://{bucket}.s3.amazonaws.com/{filename}"
    except Exception as e:
        print("S3 Error:", e)
        return None