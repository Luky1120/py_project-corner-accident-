import cv2
#0이면 노트북 내장 웹캠 숫자를 올리면 추가된 웹캠을 이용할 수 있다.
cap = cv2.VideoCapture(0)
# 3은 가로 4는 세로 길이 
cap.set(3, 720)
cap.set(4, 1080)
fc=20.0

codec=cv2.VideoWriter_fourcc('D','I','V','X')
out =cv2.VideoWriter('mycam.avi',codec,fc,(int(cap.get(3)),int(cap.get(4))))
while True:
    ret, frame = cap.read()
    cv2.imshow('test', frame)
    out.write(frame)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()