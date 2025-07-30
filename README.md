# 포트홀 2차 탐지 서버

## 1. 개요
YOLOv8을 활용하여 포트홀 객체를 최종 탐지하는 2차 검증 서버입니다.

엣지 디바이스에서 포트홀이 탐지되면, 백엔드 서버를 통해 관련 정보가 DB에 저장됩니다. 이 후, 2차 서버는 DB에서 해당 포트홀 이미지를 불러와 보다 높은 정확도의 YOLOv8 모델로 재분석하여 포트홀 여부를 최종적으로 검증합니다.

**주요 기능**
- 일정 주기로 S3에 저장된 포트홀 이미지 분석
- 포트홀 이미지에 대한 보정 처리
- DB 및 S3 기반 포트홀 데이터 관리
<br/>

## 2. 도입 배경
<table>
  <tr>
    <td align="center" width="50%">
      <img src="https://github.com/user-attachments/assets/04d0162b-e65b-4f7d-ac27-0a848f8d09b7" width="100%" height="280px"/><br/>
      <sub>나무를 포트홀로 오인식</sub>
    </td>
    <td align="center" width="50%">
      <img src="https://github.com/user-attachments/assets/ceab962e-9359-4327-832a-dcb7b2386e1f" width="100%" height="280px"/><br/>
      <sub>프레임 저하로 인한 오인식</sub>
    </td>
  </tr>
</table>
<br/>

**엣지 컴퓨팅 환경의 리소스 제약으로 인해**, 성능이 우수한 AI 모델 대신 **경량화된 YOLOv5 모델**을 엣지 디바이스에 적용하였습니다. 그러나 엣지 디바이스 단독으로 수행한 포트홀 탐지는 정확도가 낮아 한계가 있었습니다. 위 이미지에서 확인할 수 있듯이, 탐지 대상이 아닌 영역을 포트홀로 오인식하거나, 차량의 주행 속도로 인해 프레임이 저하가 발생하는 등의 문제가 반복적으로 발생햇습니다. 이러한 문제를 해결하고 보다 정밀한 검증을 수행하기 위해, 성능이 우수한 YOLO 모델을 활용한 2차 AI 서버를 도입하여 엣지 디바이스에서 탐지된 포트홀을 재검증하는 구조를 구성하였습니다.
<br/><br/>

<table>
  <tr>
    <td align="center" width="50%">
      <img width="50%" alt="chart-1753781484072" src="https://github.com/user-attachments/assets/b22348c9-24b7-4d89-a9f5-2cfc4ba85e19" /> <br/>
      <sub>YOLov5 vs. YOLOv8 성능 비교</sub>
    </td>
  </tr>
</table><br/>

## 3. 기술 스택
- Python3
- YOLOv8l
- AWS S3
- PostgreSQL
- Cron Job

## 4. 시스템 구성도
<img width="674" height="633" alt="image" src="https://github.com/user-attachments/assets/4b11c7f9-265c-40ef-9b2d-d54777179bd4" /> <br/>

### 일정 주기로 S3에 저장된 포트홀 이미지 분석
- 엣지 디바이스에서 경량 모델로 인식한 포트홀 후보 객체를 S3에서 가져와 `YOLOv8` 모델을 사용하여 검증합니다.
- 2차 검증 서버는 `cron tab` 을 이용해 일정 주기로 자동 실행됩니다.

### 포트홀 이미지에 대한 보정 처리
- 이미지의 불필요한 영역을 제거하여 오탐지를 방지합니다.

### DB 및 S3 기반 포트홀 데이터 관리
- 작업 완료 후, 사용한 로컬 이미지 및 S3 버킷 내 처리된 원본 이미지를 정리하여 스토리지와 네트워크 자원을 효율적으로 관리합니다.
- 탐지된 결과 이미지는 presigned URL을 통해 S3에 재업로드됩니다.
- 탐지되지 않는 포토홀을 기록하여, 추후 배치 작업을 통해 자동으로 삭제 처리되도록 합니다.
