from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)

# YOLOv8 모델 로드
model = YOLO("yolov8m.pt")

@app.route('/predict', methods=['POST'])
def predict():
    # 요청으로부터 이미지 로드
    file = request.files['image'].read()
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # YOLOv8 객체 탐지 수행
    results = model(img)

    # 결과를 JSON 형식으로 반환
    predictions = []
    for r in results:
        for box in r.boxes:
            predictions.append({
                "class": r.names[box.cls[0].item()],
                "confidence": box.conf[0].item(),
                "bbox": box.xyxy[0].tolist()
            })

    return jsonify(predictions)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
