import boto3
import logging
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

def s3_connection():
    ```
    s3계정과 연결
    ```
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id = os.getenv("aws_access_key_id"),
            aws_secret_access_key = os.getenv("aws_secret_access_key")
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3

def get_all_objects(s3, **base_kwargs):
    ```
    make_objects_list() 함수에서 사용
    ```
    continuation_token = None
    while True:
        list_kwargs = dict(MaxKeys=1000, **base_kwargs)
        if continuation_token:
            list_kwargs['ContinuationToken'] = continuation_token
        response = s3.list_objects_v2(**list_kwargs)
        yield from response.get('Contents', [])
        if not response.get('IsTruncated'):  
            break
        continuation_token = response.get('NextContinuationToken')

def make_objects_list(s3, BucketName):
    ```
    버킷에 존재하는 객체들을 리스트로 생성
    ```
    with open("output.txt", "w") as f:
        for file in get_all_objects(s3, Bucket=BucketName):
            f.write(file['Key']+'\n')

    with open('./output.txt', 'r') as f:
        objects_list = f.readlines()
        for idx, obj in enumerate(objects_list):
            objects_list[idx] = obj.strip()
    return objects_list

def make_object(bucketname, objectname):
    ```
    S3의 해당 버킷에서 원하는 객체의 정보를 리턴
    ```
    s3_resource = boto3.resource(
                    service_name="s3",
                    region_name="ap-northeast-2", 
                    aws_access_key_id = os.getenv("aws_access_key_id"),
                    aws_secret_access_key = os.getenv("aws_secret_access_key")
                    )
    bucket = s3_resource.Bucket(bucketname)
    return bucket.Object(objectname)

def get_object_url(s3, object):
    filename = object.key
    bucketname = object.bucket_name
    location = s3.get_bucket_location(Bucket=bucketname)["LocationConstraint"]

    return f"https://{bucketname}.s3.{location}.amazonaws.com/{filename}"

def upload_file(s3, file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    # Content_Type 미지정시 버킷에서 url 클릭하면 다운로드로 실행됨
    content_Type = 'mp4'
    try:
        if 'mp4' in file_name:
            content_Type = 'mp4'
        response = s3.upload_file(
            file_name,
            bucket,
            object_name,
            ExtraArgs={"ContentType": content_Type}
            )
    except ClientError as e:
        logging.error(e)
        return False
    return True