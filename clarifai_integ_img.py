import cv2
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import numpy as np

cap = cv2.VideoCapture('input-video/0-1.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    app = ClarifaiApp(api_key='7c4bde0867964706bf73f28d80621980')

    model = app.models.get('general-v1.3')
    image = ClImage(file_obj=open('/home/alying/PennApps/Fire-Detector/images/wildfire.jpg', 'rb'))
    response = model.predict([image])

    concepts = response['outputs'][0]['data']['concepts']
    for concept in concepts:
        print(concept['name'], concept['value'])

cap.release()
cv2.destroyAllWindows()
