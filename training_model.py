from clarifai.rest import ClarifaiApp

app = ClarifaiApp(api_key='7c4bde0867964706bf73f28d80621980')

li = ['1137.png', '802.png', '730.png', '729.png', '147.png', '1617.png', '970.png', '1233.png', '873.png', '945.png', '393.png', '465.png', '346.png', '1448.png', '1017.png', '1330.png', '537.png', '896.png', '440.png', '466.png', '1449.png', '1640.png', '562.png', '1618.png', '1641.png', '370.png', '488.png', '800.png', '1329.png', '1616.png', '1209.png', '30.png', '90.png', '1256.png', '1568.png', '1545.png', '1113.png', '536.png', '146.png', '609.png', '657.png', '1353.png', '1474.png', '369.png', '584.png', '1161.png', '1497.png', '682.png', '1210.png', '608.png', '177.png', '1018.png', '272.png', '1112.png', '754.png', '1522.png', '1401.png', '610.png', '1257.png', '1426.png', '514.png', '122.png', '417.png', '1138.png', '1258.png', '1378.png', '1402.png', '442.png', '776.png', '1305.png', '247.png', '1306.png', '1400.png', '1352.png', '1498.png', '632.png', '297.png', '777.png', '1114.png', '441.png', '728.png', '416.png', '1570.png', '210.png', '320.png', '1089.png', '848.png', '634.png', '176.png', '464.png', '394.png', '1234.png', '1592.png', '1354.png', '1232.png', '826.png', '944.png', '1642.png', '368.png', '1160.png', '1593.png', '1208.png', '704.png', '560.png', '872.png', '1186.png', '91.png', '681.png', '992.png', '824.png', '778.png', '512.png', '993.png', '1328.png', '1376.png', '825.png', '1544.png', '1185.png', '1425.png', '490.png', '148.png', '1520.png', '1162.png', '392.png', '322.png', '344.png', '968.png', '1184.png', '1064.png', '123.png', '274.png', '1594.png', '1472.png', '921.png', '1040.png', '345.png', '922.png', '561.png', '1041.png', '1665.png', '1521.png', '178.png', '209.png', '124.png', '298.png', '586.png', '705.png', '897.png', '24.png', '1065.png', '418.png', '321.png', '1016.png', '656.png', '1546.png', '680.png', '273.png', '1136.png', '898.png', '801.png', '658.png', '1042.png', '245.png', '1666.png', '538.png', '874.png', '246.png', '969.png', '1377.png', '1424.png', '1569.png', '850.png', '994.png', '920.png', '1496.png', '296.png', '513.png', '1473.png', '1090.png', '25.png', '1280.png', '946.png', '1450.png', '1304.png', '1066.png', '1281.png', '211.png', '753.png', '1282.png', '633.png', '849.png', '752.png', '1664.png', '489.png', '1088.png', '706.png', '89.png', '585.png']


for i in range(0,li.size()):
    img = ClImage(filename='/home/alying/PennApps/Fire-Detector/datasetGen/'+li[i])

app.inputs.bulk_create_images([img1

model = app.models.create(model_id="puppy", concepts=["my puppy"])

model.train()

model = app.models.get('puppy')
model.predict_by_url('https://samples.clarifai.com/metro-north.jpg')
