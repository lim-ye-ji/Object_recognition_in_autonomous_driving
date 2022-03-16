# -*- coding: utf-8 -*-
import os
from traffic_light_module import *

# +
# 추출 전 데이터 위치
# path = "/Users/yu/tf39_test/실습/자율주행_신호등인식/train/데이터/[원천]d_train_1920_1080_daylight_1/"
path = './trainingData/training/test/'

# 추출 후 저장할 데이터 위치
path_g = './validationData/green/'
path_y = './validationData/yellow/'
path_r = './validationData/red/'
# -

light_list = os.listdir(path)

# +
first_detect = []

for img in light_list:
    if img == ".DS_Store":
        continue
        
    # ROI 지정, x,y,w,h ,N 설정 완료
    x1 = 300
    y1 = 0
    w1 = 1400
    h1 = 500
    
    green(path, img, X = x1, Y = y1, W = w1, H = h1, first_detect = first_detect, path_g = path_g)
    yellow(path, img, X = x1, Y = y1, W = w1, H = h1, first_detect = first_detect, path_y = path_y)
    red(path, img, X = x1, Y = y1, W = w1, H = h1, first_detect = first_detect, path_r = path_r)
# -



