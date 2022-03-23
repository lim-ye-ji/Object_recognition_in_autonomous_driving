# traffic_light_detection-recognition

~module 은 함수만 모아놓음

~detection 은 함수들 실행 코드

## 사용방법
1. module 들어가서 신호등 색깔 별로 검출해서 저장할 path 경로들을 알맞게 지정
2. detection 들어가서 path에 원본 데이터가 있는 경로를 지정
3. detection 실행하면 된다

## 주의사항
module, detection은 반드시 같은 폴더에 위치해야 함

## 문제 점들
+ 실행 중간에 error: (-215:Assertion failed) !_img.empty() in function 'imwrite' 에러남
-> 해결
+ 엉뚱한 구역을 신호등을 인식하는 문제
-> 컨투어 과정에 추가 규칙이 필요(ROI 평균, 정중앙 색의값...)_해결중
