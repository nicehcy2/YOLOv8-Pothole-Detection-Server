import requests


def get_presigned_url(presigned_url_api):
    try:
        response = requests.get(presigned_url_api)
        response.raise_for_status()
        data = response.json()
        return data['presignedUrl'], data['fileUrl']
    except requests.RequestException as e:
        print(f"Failed to get presigned URL: {e}")
        return None, None


def upload_image_to_s3(presigned_url, file_path):
    try:
        with open(file_path, 'rb') as file:
            response = requests.put(presigned_url, data=file)
            response.raise_for_status()
            print(f"Successfully uploaded {file_path} to S3.")
    except requests.RequestException as e:
        print(f"Failed to upload {file_path} to S3: {e}")
        
    return presigned_url

# latitude와 longitude는 어떻게 처리해야될 지 고민

'''
def register_image_url(file_url):
    try:
        # 요청할 데이터 생성
        data = {
            'latitude': latitude,
            'longitude': longitude,
            'imageUrl': file_url
        }

        # POST 요청 보내기
        response = requests.post(file_url_registration_api, json=data)
        response.raise_for_status()
        print(f"Successfully registered image URL: {file_url}")

    except requests.RequestException as e:
        print(f"Failed to register image URL {file_url}: {e}")
'''