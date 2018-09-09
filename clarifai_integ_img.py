from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='7c4bde0867964706bf73f28d80621980')

model = app.models.get('general-v1.3')
image = ClImage(file_obj=open('/home/alying/PennApps/Fire-Detector/images/wildfire.jpg', 'rb'))
response = model.predict([image])

concepts = response['outputs'][0]['data']['concepts']
for concept in concepts:
    print(concept['name'], concept['value'])
