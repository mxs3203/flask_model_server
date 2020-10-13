from io import BytesIO
import json
import requests
from PIL import Image
print("Wrong pass example")
url = 'http://localhost:5000/api/login'
r = requests.post(url,json={'username': 'filipos', 'password':'krivipass'})
print(r.status_code)


print("Correct login example")
url = 'http://localhost:5000/api/login'
r = requests.post(url,json={'username': 'filipos', 'password':'Krastavac56'})
print(json.loads(r.content.decode("utf-8")))
token = json.loads(r.content.decode("utf-8"))['token']

print("Send Xray Img example")
url = 'http://localhost:5000/models/xray'
my_img = {'image': open('test1.jpg', 'rb')}
headers = {'token': token}
headers = headers
r = requests.post(url, files=my_img, headers=headers)
print(r.status_code)
stream = BytesIO(r.content)
image = Image.open(stream).convert("RGBA")
image.save("1.png")
stream.close()
#
#
url = 'http://localhost:5000/models/coccidia'
my_img = {'image': open('test2.jpg', 'rb')}
r = requests.post(url, files=my_img)
print(r.status_code)
stream = BytesIO(r.content)
image = Image.open(stream).convert("RGBA")
image.save("2.png")
stream.close()

url = 'http://localhost:5000/models/neutrophil'
my_img = {'image': open('test3.jpg', 'rb')}
r = requests.post(url, files=my_img)
print(r.status_code)
stream = BytesIO(r.content)
image = Image.open(stream).convert("RGBA")
stream.close()
image.save("3.png")


