import twilio_sms
import cv2
import numpy as np
import time 
import app
from flask import Flask, request, render_template

#@app.route('/fire/')
def fire_info(vid_no):
    #print(vid_no, type(vid_no))
    vid = int(vid_no) 
    #input("Video number: ")

    vid_options = {1: 'static/0-1.mp4',
                   2: 'static/1-0.mp4',
                   3: 'static/2-0.mp4',
                   4: 'static/3.mp4'}    
        
    path = vid_options[vid]
    cap = cv2.VideoCapture(path)

    start = time.time()
    text_sent = False
    while True:
        (grabbed, frame) = cap.read()
        if not grabbed:
            break
        
        cv2.imshow('Original Video', frame)
         
        blur = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
     
        lower = [18, 50, 50]
        upper = [35, 255, 255]
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        mask = cv2.inRange(hsv, lower, upper)
         
        output = cv2.bitwise_and(frame, hsv, mask=mask)
        no_red = cv2.countNonZero(mask)
        no_black = cv2.countNonZero(cv2.bitwise_not(mask, mask))

        #cv2.imshow("mask", mask)
        cv2.imshow("Fire Detection", output)
        
        total = no_black + no_red #frame.size
        percentage = float(no_red)/total
        current = time.time()
        
        time_elapsed = current - start

        rate_of_spread = float(percentage) / time_elapsed
        print("Rate of spread: {}px%/sec".format(rate_of_spread))
        #print(no_red)
        #print(total)
        print("Size: {0:.0f}%".format(percentage * 100))

        if int(no_red) > 5 and not text_sent: #approx. greater than 10%
            print("test")
            twilio_sms.send_text('Warning: possible wildfire near you!')
            text_sent = True
            #cv2.waitKey(3000)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()

if(__name__ == '__main__'):
    fire_info()
