from io import BytesIO

import requests
from PIL import Image

url = 'http://localhost:5000/api/xray'
my_img = {'image': open('test1.jpg', 'rb')}
r = requests.post(url, files=my_img)
print(r.status_code)
stream = BytesIO(r.content)
image = Image.open(stream).convert("RGBA")
image.save("1.png")
stream.close()


url = 'http://localhost:5000/api/coccidia'
my_img = {'image': open('test2.jpg', 'rb')}
r = requests.post(url, files=my_img)
print(r.status_code)
stream = BytesIO(r.content)
image = Image.open(stream).convert("RGBA")
image.save("2.png")
stream.close()

url = 'http://localhost:5000/api/neutrophil'
my_img = {'image': open('test3.jpg', 'rb')}
r = requests.post(url, files=my_img)
print(r.status_code)
stream = BytesIO(r.content)
image = Image.open(stream).convert("RGBA")
stream.close()
image.save("3.png")