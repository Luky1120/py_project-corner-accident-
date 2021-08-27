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
        ret, c = cap.read()
        c= cv2.flip(c,1) 
        

        # apply object detection (물체 검출)
        bbox, label, conf = cv.detect_common_objects(a, confidence=0.25, model='yolov4-tiny')
        
        # draw bounding box over detected objects (검출된 물체 가장자리에 바운딩 박스 그리기)
        out = draw_bbox(a, bbox, label, conf, write_conf=True)

        cv2.imshow("Real-time object detection", out)

        draw = c.copy()

        if not ret:
            break
        
        face, confidence = cv.detect_face(c)
 
    print(face)
    print(confidence)
 
    # loop through detected faces
    for idx, f in enumerate(face):
        
        (startX, startY) = f[0], f[1]
        (endX, endY) = f[2], f[3]
 
        '모자이크 효과 주기: 얼굴 부분을 줄였다가 다시 원크기로 복구시키면 모자이크처럼 됨.'
        face_region = c[startY:endY, startX:endX]
        
        M = face_region.shape[0]
        N = face_region.shape[1]
 
        face_region = cv2.resize(face_region, None, fx=0.05, fy=0.05, interpolation=cv2.INTER_AREA)
        face_region = cv2.resize(face_region, (N, M), interpolation=cv2.INTER_AREA)
        c[startY:endY, startX:endX] = face_region



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
        nc=label.count('car') 
        person( diff_cnt, max_diff,npe,nc)
        

        if diff_cnt > max_diff:
            nzero = np.nonzero(diff)
            cv2.rectangle(draw, (min(nzero[1]), min(nzero[0])),
                          (max(nzero[1]), max(nzero[0])), (0, 255, 0), 2)

            cv2.putText(draw, "Motion detected!!", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
            
 
        stacked = np.hstack((draw, cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)))
        
        #cv2.imshow('motion', stacked)
 
        a = b
        b = c
 
        if cv2.waitKey(1) & 0xFF == 27:
            break