import numpy as np
import cv2

path = input("Video path: ")

cap = cv2.VideoCapture(path)

while(cap.isOpened()):
    ret, frame = cap.read()

    if frame is None:
        break

    cv2.imshow('frame', frame)
    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame_gray', frame_gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
