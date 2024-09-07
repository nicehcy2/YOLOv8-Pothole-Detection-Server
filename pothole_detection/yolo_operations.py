import os
import cv2
from ultralytics import YOLO

pothole_class_id = 1


def detect_pothole(input_image_dir, output_image_dir, model_path='bestv8m.pt'):
    model = YOLO(model_path)

    # 출력 이미지 디렉토리 생성
    os.makedirs(output_image_dir, exist_ok=True)

    # 폴더 내 모든 이미지 파일 가져오기
    image_files = [f for f in os.listdir(
        input_image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        # 이미지 파일 경로
        image_path = os.path.join(input_image_dir, image_file)

        # 이미지 읽기
        image = cv2.imread(image_path)

        # 이미지 크기
        height, width, _ = image.shape

        # 이미지의 하단 1/2 추출
        lower_half = image[int(height / 2):, :]

        # 하단 1/2 이미지에서 객체 탐지
        results = model(lower_half)

        # 포트홀 감지 여부 확인
        pothole_detected = False
        for box in results[0].boxes:
            if box.cls.item() == pothole_class_id:
                pothole_detected = True
                break

        # 탐지된 객체가 있는 경우
        if len(results[0].boxes) > 0 and pothole_detected:
            # 탐지 결과 시각화
            annotated_image = results[0].plot()  # 탐지된 객체를 이미지에 시각화
            # 원본 이미지의 하단 1/2 부분에 시각화된 하단 이미지를 덮어쓰기
            image[int(height / 2):, :] = annotated_image

            # 결과 이미지 파일 이름 생성
            output_image_file = f"{os.path.splitext(image_file)[0]}.jpg"
            output_image_path = os.path.join(
                output_image_dir, output_image_file)

            # 결과 이미지 저장
            cv2.imwrite(output_image_path, image)
            print(f"Saved {output_image_path}")
