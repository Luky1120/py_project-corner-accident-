# import necessary packages
import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
import time
# open stream
import cv2
import numpy as np
# main문 import
from main import *
 
thresh = 25
max_diff = 5
 
a, b, c = None, None, None
 
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('test.mp4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
 
if cap.isOpened():
    ret, a = cap.read()
    a= cv2.flip(a,1) 
    ret, b = cap.read()
    b = cv2.flip(b,1) 

    while ret:
        status, frame = cap.read()
        frame= cv2.flip(frame,1) 
        ret, c = cap.read()
        c= cv2.flip(c,1) 
        

        # apply object detection (물체 검출)
        bbox, label, conf = cv.detect_common_objects(frame, confidence=0.25, model='yolov4-tiny')

        # draw bounding box over detected objects (검출된 물체 가장자리에 바운딩 박스 그리기)
        out = draw_bbox(frame, bbox, label, conf, write_conf=True)

        cv2.imshow("Real-time object detection", out)

        draw = c.copy()

        if not ret:
            break
 
        a_gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
        b_gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
        c_gray = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
 
        diff1 = cv2.absdiff(a_gray, b_gray)
        diff2 = cv2.absdiff(b_gray, c_gray)
 
        ret, diff1_t = cv2.threshold(diff1, thresh, 255, cv2.THRESH_BINARY)
        ret, diff2_t = cv2.threshold(diff2, thresh, 255, cv2.THRESH_BINARY)
 
        diff = cv2.bitwise_and(diff1_t, diff2_t)
 
        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)

        diff_cnt = cv2.countNonZero(diff)
        npe=label.count('person') 
        nc=label.count('phone') 
        person( diff_cnt, max_diff,npe,nc)
        

        if diff_cnt > max_diff:
            nzero = np.nonzero(diff)
            cv2.rectangle(draw, (min(nzero[1]), min(nzero[0])),
                          (max(nzero[1]), max(nzero[0])), (0, 255, 0), 2)
 
            '''
            rectangle: pt1, pt2 기준으로 사각형 프레임을 만들어줌.
            nzero: diff는 카메라 영상과 사이즈가 같으며, a, b프레임의 차이 어레이를 의미함.
            (min(nzero[1]), min(nzero[0]): diff에서 0이 아닌 값 중 행, 열이 가장 작은 포인트
            (max(nzero[1]), max(nzero[0]): diff에서 0이 아닌 값 중 행, 열이 가장 큰 포인트
            (0, 255, 0): 사각형을 그릴 색상 값
            2 : thickness
            '''

            cv2.putText(draw, "Motion detected!!", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
            
 
        stacked = np.hstack((draw, cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)))
        
        cv2.imshow('motion', stacked)
 
        a = b
        b = c
 
        if cv2.waitKey(1) & 0xFF == 27:
            break

