# -*- coding: utf-8 -*-
import cv2

# # green yellow red 모델들

# 파일명 시작 숫자 설정
# N_1 = 1
# N_2 = 1
# N_3 = 1
seq = 1 # 채번 변수 통일 20220308 by yjlim

# 추출 이미지 저장 위치 설정
path_g = '/Users/yu/tf39_test/실습/자율주행_신호등인식/data/green/'
path_y = '/Users/yu/tf39_test/실습/자율주행_신호등인식/data/yellow/'
path_r = '/Users/yu/tf39_test/실습/자율주행_신호등인식/data/red/'


def green(img,X,Y,W,H):
    global seq, path_g
    ## 파일 불러오기
    B = cv2.imread(img, cv2.IMREAD_COLOR)
    
    # ROI 지정
    roi = B[Y:Y+H, X:X+W]
    roi2 = roi.copy()

    ## 초록색 부분 추출
    # hsv 영역 전환
    roi2_hsv = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)

    # 색 범위 지정
    low = (43, 40, 120)
    up = (95, 255, 255)

    # 범위내의 픽셀들은 흰색, 나머지 검은색
    roi2_mask = cv2.inRange(roi2_hsv, low, up)
    
    # 바이너리 이미지를 마스크로 사용하여 원본이미지에서 범위값에 해당하는 영상부분을 획득
    roi2_result = cv2.bitwise_and(roi2, roi2, mask=roi2_mask)

    ## 모폴 침식 사용
    # 구조화 요소 커널, 사각형 (2x2) 생성 # 3x3으로 수정
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    
    # 열림 연산 적용 # yjlim 추가
    erosion1 = cv2.morphologyEx(roi2_result, cv2.MORPH_OPEN, k)
    
    # 침식 연산 적용
    erosion2 = cv2.erode(roi2_result, k)
    
    erosion3 = erosion1.copy()

    ## 색 영역 변환
    # FindContours support only 8uC1 and 32sC1 images,
    # HSV 이미지는 contour 기능을 쓸 수 없으므로 HSV->BGR->GRAY 로 전환하자
    erosion3 = cv2.cvtColor(erosion3, cv2.COLOR_HSV2BGR)
    erosion3 = cv2.cvtColor(erosion3, cv2.COLOR_BGR2GRAY)

    ## contour 직사각형으로 출력
    position = []
    contours, hierarchy = cv2.findContours(erosion3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # cnt를 일일이 확인해서 좌표상으로 크게 차이 안나는 것들(잡음)은 추가안함(너무 작은 직사각형, 한쪽으로 길쭉한 직사각형 제외)
        if (w >= 8) and (h >= 8) and (abs(w - h) <= 4):
            cv2.rectangle(erosion3, (x, y), (x + w, y + h), (255, 0, 0), 1)
            position.append((x, y, w, h))

    ## 추출한 신호등만 별도의 이미지로 저장
    if position:
        for a in position:
            # 가로, 세로 높이 비교해서 큰 값으로 길이 설정 # yjlim
            if a[2] >= a[3]:
                length = a[2]
            else:
                length = a[3]
                
            interval_x = int(length / 3) # 너비 3등분
            interval_y = int(a[3] / 3) # 높이 3등분
            
            if a[1] - interval_y > 0 and X + a[0] - 2 * length - 2 * interval_x > 0:
                real3 = B[a[1] - interval_y:a[1] + a[3] + interval_y,\
                        X + a[0] - 2 * length - 2 * interval_x:X + a[0] + length + interval_x]
                print(img +'///G' + str(seq) + '.jpg')
                cv2.imwrite(path_g + str(seq) + '.jpg', real3)
                seq = seq + 1


def yellow(img,X,Y,W,H):
    global seq, path_y
    ## 파일 불러오기
    B = cv2.imread(img, cv2.IMREAD_COLOR)
    # ROI 지정
    roi = B[Y:Y+H,X:X+W]
    roi2 = roi.copy()

    ## 노랑색 부분 추출
    # hsv 영역 전환
    roi2_hsv = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)

    # 색 범위 지정
    low = (10, 10, 110)
    up = (31, 255, 255)

    roi2_mask = cv2.inRange(roi2_hsv, low, up)
    roi2_result = cv2.bitwise_and(roi2, roi2, mask=roi2_mask)

    ## 모폴 침식 사용
    # 구조화 요소 커널, 사각형 (2x2) 생성
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    
    # 열림 연산 적용 # yjlim 추가
    erosion1 = cv2.morphologyEx(roi2_result, cv2.MORPH_OPEN, k)
    
    # 침식 연산 적용
    erosion = cv2.erode(roi2_result, k)
    
    erosion3 = erosion1.copy()

    ## 색 영역 변환
    # FindContours support only 8uC1 and 32sC1 images,
    # HSV 이미지는 contour 기능을 쓸 수 없으므로 HSV->BGR->GRAY 로 전환하자
    erosion3 = cv2.cvtColor(erosion3, cv2.COLOR_HSV2BGR)
    erosion3 = cv2.cvtColor(erosion3, cv2.COLOR_BGR2GRAY)

    ## contour 직사각형으로 출력
    position = []
    contours, hierarchy = cv2.findContours(erosion3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # cnt를 일일이 확인해서 좌표상으로 크게 차이 안나는 것들(잡음)은 추가안함(너무 작은 직사각형, 한쪽으로 길쭉한 직사각형 제외)
        if (w >= 8) and (h >= 8) and (abs(w - h) <= 4):
            cv2.rectangle(erosion3, (x, y), (x + w, y + h), (255, 0, 0), 1)
            position.append((x, y, w, h))

    ## 추출한 신호등만 별도의 이미지로 저장
    if position:
        for a in position:
            # 가로, 세로 높이 비교해서 큰 값으로 길이 설정 # yjlim
            if a[2] >= a[3]:
                length = a[2]
            else:
                length = a[3]
                
            interval_x = int(length / 3) # 너비 3등분
            interval_y = int(a[3] / 3) # 높이 3등분
            
            if a[1] - interval_y > 0 and X + a[0] - length - interval_x > 0:
                real3 = B[a[1] - interval_y:a[1] + a[3] + interval_y,
                        X + a[0] - length - interval_x:X + a[0] + 2 * length + interval_x]
                print(img + '///Y' + str(seq) + '.jpg')
                cv2.imwrite(path_y + str(seq) + '.jpg', real3)
                seq = seq + 1

# ###########

def red(img,X,Y,W,H):
    global seq, path_r
    
    ## 파일 불러오기
    B = cv2.imread(img, cv2.IMREAD_COLOR)
    
    # ROI 지정
    roi = B[Y:Y+H,X:X+W]
    roi2 = roi.copy()

    ## 빨강색 부분 추출
    # hsv 영역 전환
    roi2_hsv = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)

    # 색 범위 지정
    low = (0, 30,50)
    up = (10, 255, 255)

    roi2_mask = cv2.inRange(roi2_hsv, low, up)
    roi2_result = cv2.bitwise_and(roi2, roi2, mask=roi2_mask)

    ## 모폴 침식 사용
    # 구조화 요소 커널, 사각형 (2x2) 생성
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    
    # 열림 연산 적용 # yjlim 추가
    erosion1 = cv2.morphologyEx(roi2_result, cv2.MORPH_OPEN, k)
    
    # 침식 연산 적용
    erosion = cv2.erode(roi2_result, k)
    
    erosion3 = erosion1.copy()

    ## 색 영역 변환
    # FindContours support only 8uC1 and 32sC1 images,
    # HSV 이미지는 contour 기능을 쓸 수 없으므로 HSV->BGR->GRAY 로 전환하자
    erosion3 = cv2.cvtColor(erosion3, cv2.COLOR_HSV2BGR)
    erosion3 = cv2.cvtColor(erosion3, cv2.COLOR_BGR2GRAY)

    ## contour 직사각형으로 출력
    position = []
    contours, hierarchy = cv2.findContours(erosion3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # cnt를 일일이 확인해서 좌표상으로 크게 차이 안나는 것들(잡음)은 추가안함(너무 작은 직사각형, 한쪽으로 길쭉한 직사각형 제외)
        if (w >= 8) and (h >= 8) and (abs(w - h) <= 4):
            cv2.rectangle(erosion3, (x, y), (x + w, y + h), (255, 0, 0), 1)
            position.append((x, y, w, h))

    ## 추출한 신호등만 별도의 이미지로 저장
    if position:
        for a in position:
            # 가로, 세로 높이 비교해서 큰 값으로 길이 설정 # yjlim
            if a[2] >= a[3]:
                length = a[2]
            else:
                length = a[3]
                
            interval_x = int(length / 3) # 너비 3등분
            interval_y = int(a[3] / 3) # 높이 3등분
            
            if a[1] - interval_y > 0 and X + a[0] - interval_x > 0:
                real3 = B[a[1] - interval_y:a[1] + a[3] + interval_y,
                        X + a[0] - interval_x:X + a[0] + 3 * length + 2 * interval_x]
                print(img + '///R' + str(seq) + '.jpg')
                cv2.imwrite(path_r + str(seq) + '.jpg', real3)
                seq = seq + 1

    else:
        ## 빨강색 부분 추출2
        # 다시 hsv 영역 전환
        roi2_hsv = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)

        # 색 범위 지정2
        low = (150, 40, 50)
        up = (180, 255, 255)

        roi2_mask = cv2.inRange(roi2_hsv, low, up)
        roi2_result = cv2.bitwise_and(roi2, roi2, mask=roi2_mask)

        ## 모폴 침식 사용
        # 구조화 요소 커널, 사각형 (2x2) 생성
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        
        # 열림 연산 적용 # yjlim 추가
        erosion1 = cv2.morphologyEx(roi2_result, cv2.MORPH_OPEN, k)
        
        # 침식 연산 적용
        erosion = cv2.erode(roi2_result, k)
        
        erosion3 = erosion1.copy()

        ## 색 영역 변환
        # FindContours support only 8uC1 and 32sC1 images,
        # HSV 이미지는 contour 기능을 쓸 수 없으므로 HSV->BGR->GRAY 로 전환하자
        erosion3 = cv2.cvtColor(erosion3, cv2.COLOR_HSV2BGR)
        erosion3 = cv2.cvtColor(erosion3, cv2.COLOR_BGR2GRAY)

        ## contour 직사각형으로 출력
        position = []
        contours, hierarchy = cv2.findContours(erosion3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # cnt를 일일이 확인해서 좌표상으로 크게 차이 안나는 것들(잡음)은 추가안함(너무 작은 직사각형, 한쪽으로 길쭉한 직사각형 제외)
            if (w >= 8) and (h >= 8) and (abs(w - h) <= 4):
                cv2.rectangle(erosion3, (x, y), (x + w, y + h), (255, 0, 0), 1)
                position.append((x, y, w, h))

        if position:
            for a in position:
                # 가로, 세로 높이 비교해서 큰 값으로 길이 설정 # yjlim
                if a[2] >= a[3]:
                    length = a[2]
                else:
                    length = a[3]

                interval_x = int(length / 3) # 너비 3등분
                interval_y = int(a[3] / 3) # 높이 3등분
                
                if a[1] - interval_y > 0 and X + a[0] - interval_x > 0:
                    real3 = B[a[1] - interval_y:a[1] + a[3] + interval_y,
                            X + a[0] - interval_x:X + a[0] + 3 * length + 2 * interval_x]
                    print(img + '///R' + str(seq) + '.jpg')
                    cv2.imwrite(path_r + str(seq) + '.jpg', real3)
                    seq = seq + 1