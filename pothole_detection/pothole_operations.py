import os
import requests


def get_pothole_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to get pothole data: {e}")
        return []


def process_pothole_data(pothole_data, output_image_dir, post_api_url, delete_api_url):
    for pothole in pothole_data:
        image_url = pothole.get('imageUrl')
        if not image_url:
            continue

        # 이미지 파일 이름 추출
        image_file_name = os.path.basename(image_url)
        image_file_path = os.path.join(output_image_dir, image_file_name)

        if os.path.isfile(image_file_path):
            # 이미지 파일이 존재할 경우 POST 요청
            post_request(image_url, post_api_url)
        else:
            # 이미지 파일이 존재하지 않을 경우 DELETE 요청
            delete_request(image_url, delete_api_url)


def post_request(image_url, api_url):
    try:
        response = requests.post(api_url, json={'imageUrl': image_url})
        response.raise_for_status()
        print(f"Successfully posted image URL: {image_url}")
    except requests.RequestException as e:
        print(f"Failed to post image URL {image_url}: {e}")


def delete_request(image_url, api_url):
    try:
        response = requests.delete(api_url, json={'imageUrl': image_url})
        response.raise_for_status()
        print(f"Successfully deleted image URL: {image_url}")
    except requests.RequestException as e:
        print(f"Failed to delete image URL {image_url}: {e}")
