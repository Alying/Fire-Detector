import clarifai
from clarifai.rest import ClarifaiApp
from clarifai.rest import Video as ClVideo

app = ClarifaiApp(api_key='7c4bde0867964706bf73f28d80621980')

model = app.models.get('general-v1.3')
video = ClVideo(filename='/home/alying/PennApps/Fire-Detector/input-video/0-1.mp4')
model.predict([video])
