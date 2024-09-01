from ultralytics import YOLO
import cv2
import os

model = YOLO('bestv8m.pt')

input_video_path = '/content/input_video.mp4'  # Google Drive에 있는 동영상 파일 경로
output_image_dir = '/content/output_images2/'  # Google Drive에 저장할 이미지 디렉토리

# 출력 이미지 디렉토리 생성
os.makedirs(output_image_dir, exist_ok=True)

# OpenCV 비디오 캡처
cap = cv2.VideoCapture(input_video_path)

# 프레임 번호 초기화
frame_number = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 이미지 객체 탐지
    results = model(frame)

    # 탐지된 객체가 있는 경우
    if len(results[0].boxes) > 0:
        # 탐지 결과 시각화
        annotated_image = results[0].plot()  # 탐지된 객체를 이미지에 시각화

        # 이미지 파일 이름 생성
        image_file_name = f"frame_{frame_number:04d}.jpg"
        image_file_path = os.path.join(output_image_dir, image_file_name)

        # 이미지 저장
        cv2.imwrite(image_file_path, annotated_image)
        print(f"Saved {image_file_path}")

    # 프레임 번호 증가
    frame_number += 1

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
