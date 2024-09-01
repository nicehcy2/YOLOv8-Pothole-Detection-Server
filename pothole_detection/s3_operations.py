import os
import boto3
from botocore.exceptions import ClientError

# S3 리소스 생성
s3 = boto3.resource('s3')

# s3 파일을 로컬에 다운로드


def download_s3_files(bucket_name, s3_edge_folder, input_image_dir):

    # S3 버킷 객체
    bucket = s3.Bucket(bucket_name)
    
    # 폴더 내 모든 객체 다운로드
    for obj in bucket.objects.filter(Prefix=s3_edge_folder):
        # S3 객체 키 (파일 경로)
        s3_key = obj.key

        # 파일 이름 추출
        file_name = os.path.relpath(s3_key, s3_edge_folder)

        # 로컬 경로 설정
        local_file_path = os.path.join(input_image_dir, file_name)

        # 로컬에 필요한 디렉토리가 없으면 생성
        if not os.path.exists(os.path.dirname(local_file_path)):
            os.makedirs(os.path.dirname(local_file_path))

        # 파일 다운로드
        if not obj.key.endswith('/') and obj.size > 0:
            if (obj.key.endswith(('.png', '.jpg', '.jpeg'))):
                bucket.download_file(s3_key, local_file_path)
                print(f"Downloaded {s3_key} to {local_file_path}")

    print("All files have been downloaded successfully.")

# S3에서 파일 삭제


def delete_s3_files(bucket_name, s3_folder, local_dir):
    bucket = s3.Bucket(bucket_name)

    for root, dirs, files in os.walk(local_dir, topdown=False):
        for file in files:
            relative_path = os.path.relpath(
                os.path.join(root, file), local_dir)
            s3_key = os.path.join(s3_folder, relative_path)

            try:
                bucket.Object(s3_key).delete()
                print(f"Deleted S3 object: {s3_key}")
            except ClientError as e:
                print(f"Failed to delete S3 object {s3_key}: {e}")
