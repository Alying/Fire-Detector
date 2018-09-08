import numpy as np
import cv2

path = 'input-video/fire1.mp4'

cap = cv2.VideoCapture(path)

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    cv2.imwrite('test.png',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
