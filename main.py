from pothole_detection.s3_operations import download_s3_files, delete_s3_files
from pothole_detection.yolo_operations import detect_pothole
from pothole_detection.presigned_url import get_presigned_url, upload_image_to_s3
from pothole_detection.utils import delete_local_files
from pothole_detection.pothole_operations import get_pothole_data, process_pothole_data
import os

# Configuration
base_url = 'https://api.rootcodepothole.com/'

bucket_name = 'rootcode-s3bucket'
s3_edge_folder = 'pothole/'
input_image_dir = './input_potholes/'
output_image_dir = './output_potholes/'
presigned_url_api = base_url + 'presigned-validate-url'
# file_url_registration_api = base_url + 'register'

pothole_data_api = base_url + 'images/unverified'
post_api_url = base_url + 'potholes/second-verification'

valid_file_urls = []

# Download files from S3
download_s3_files(bucket_name, s3_edge_folder, input_image_dir)

# Detect potholes using YOLO
detect_pothole(input_image_dir, output_image_dir)

# Process and upload detected images


def process_images():
    image_files = [f for f in os.listdir(
        output_image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        file_path = os.path.join(output_image_dir, image_file)

        presigned_url, file_url = get_presigned_url(presigned_url_api)
        if presigned_url is None or file_url is None:
            print(f"Skipping file {file_path} due to URL fetching failure.")
            continue

        valid_file_urls.append(upload_image_to_s3(presigned_url, file_path))


process_images()

update_valid_file_urls = []
for url in valid_file_urls:
    update_valid_file_urls.append(url.split('?')[0])

# Get pothole data and process it
pothole_data = get_pothole_data(pothole_data_api)
process_pothole_data(pothole_data, output_image_dir,
                     post_api_url, update_valid_file_urls)

# Cleanup
delete_s3_files(bucket_name, s3_edge_folder, input_image_dir)
delete_local_files(input_image_dir)
delete_local_files(output_image_dir)
