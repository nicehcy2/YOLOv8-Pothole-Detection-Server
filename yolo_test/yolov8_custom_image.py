from ultralytics import YOLO
import cv2
import os

model = YOLO('bestv8m.pt')

# 이미지 폴더 경로 및 출력 디렉토리 설정
input_folder_path = '/content/output_images/'  # 이미지 파일이 있는 폴더 경로
output_image_dir = '/content/output_images5/'  # 결과 이미지 저장 디렉토리

# 출력 이미지 디렉토리 생성
os.makedirs(output_image_dir, exist_ok=True)

# 폴더 내 모든 이미지 파일 가져오기
image_files = [f for f in os.listdir(
    input_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

for image_file in image_files:
    # 이미지 파일 경로
    image_path = os.path.join(input_folder_path, image_file)

    # 이미지 읽기
    image = cv2.imread(image_path)

    # 이미지 크기
    height, width, _ = image.shape

    # 이미지의 하단 2/3 추출
    lower_two_thirds = image[int(height / 2):, :]

    # 하단 2/3 이미지에서 객체 탐지
    results = model(lower_two_thirds)

    # 탐지된 객체가 있는 경우
    if len(results[0].boxes) > 0:
        # 탐지 결과 시각화
        annotated_image = results[0].plot()  # 탐지된 객체를 이미지에 시각화

        # 결과 이미지 파일 이름 생성
        output_image_file = f"{os.path.splitext(image_file)[0]}_lower_two_thirds.jpg"
        output_image_path = os.path.join(output_image_dir, output_image_file)

        # 결과 이미지 저장
        cv2.imwrite(output_image_path, annotated_image)
        print(f"Saved {output_image_path}")
