# import necessary packages
import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
import time
print(cv2.__version__)
# open stream
url='http://192.168.0.136:9090/?action=stream'
stream = cv2.VideoCapture(url)


# loop through frames
while True:
    # read frame from stream 
    status, frame = stream.read()

    if not status:
        break

    # apply object detection (물체 검출)
    bbox, label, conf = cv.detect_common_objects(frame)

    print(bbox, label, conf)

    # draw bounding box over detected objects (검출된 물체 가장자리에 바운딩 박스 그리기)
    out = draw_bbox(frame, bbox, label, conf, write_conf=True)

    # display output
    cv2.imshow("Real-time object detection", out)

    # press "Q" to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# release resources
stream.release()
cv2.destroyAllWindows()   