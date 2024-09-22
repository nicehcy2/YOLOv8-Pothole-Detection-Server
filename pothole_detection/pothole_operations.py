import os
import requests
import json

def get_pothole_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to get pothole data: {e}")
        return []


def process_pothole_data(pothole_data, output_image_dir, post_api_url, update_valid_file_urls):
    
    valid_pothole_ids = []
    invalid_pothole_ids = []
    
    if (pothole_data == None): 
        print("null")
        return
    
    for pothole in pothole_data.get("images", []):
        image_url = pothole.get('url')
        if not image_url:
            continue

        # 이미지 파일 이름 추출
        image_file_name = os.path.basename(image_url)
        image_file_path = os.path.join(output_image_dir, image_file_name)
        print(image_file_path)
        
        if os.path.isfile(image_file_path):
            # 이미지 파일이 존재할 경우 validPotholeIds에 ID 추가
            valid_pothole_ids.append(pothole.get("potholeId"))
        else:
            # 이미지 파일이 존재하지 않을 경우 invalidPotholeIds에 ID 추가
            invalid_pothole_ids.append(pothole.get("potholeId"))
    
    # SecondVerificationRequestDTO에 해당하는 데이터 형식
    data_to_send = {
        "validPotholeIds": valid_pothole_ids,
        "invalidPotholeIds": invalid_pothole_ids,
        "potholeUrl": update_valid_file_urls
    }
    
    print(valid_pothole_ids)
    print(update_valid_file_urls)

    # 데이터를 서버로 POST 요청 보내기
    response = requests.post(
        url=post_api_url,  # 서버 URL
        headers={'Content-Type': 'application/json'},  # JSON 형식으로 전송
        data=json.dumps(data_to_send)  # 데이터를 JSON 형식으로 변환하여 전송
    )


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
