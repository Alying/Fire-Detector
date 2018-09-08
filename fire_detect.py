import cv2
import numpy as np
 
#video_file = "video_1.mp4"
path = input("Video path: ")

cap = cv2.VideoCapture(path)
 
while True:
    (grabbed, frame) = cap.read()
    if not grabbed:
        break
 
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
 
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)
     
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    no_red = cv2.countNonZero(mask)
    no_black = cv2.countNonZero(cv2.bitwise_not(no_red))

    cv2.imshow("mask", mask)
    cv2.imshow("output", output)
    
    total = no_black + no_red#frame.size
    percentage = float(no_red)/total
    print(no_red)
    print(total)
    print("{0:.0f}%".format(percentage*100))

    if int(no_red) > 20000:
        print ('Fire detected')
        cv2.waitKey(3000)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cv2.destroyAllWindows()
cap.release()
