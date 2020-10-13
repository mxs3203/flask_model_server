from io import BytesIO
import json
import requests
from PIL import Image
import os
import unittest

class TestLoginAPI(unittest.TestCase):
    def test_incorrect_login(self):
        print("Wrong pass example")
        url = 'http://overunderapi.ddns.net:5655/api/login'
        r = requests.post(url,json={'username': 'filipos', 'password':'krivipass'})
        print(r.status_code)
        self.assertEqual(r.status_code, 401)

    def test_correct_login(self):
        print("Correct login example")
        url = 'http://overunderapi.ddns.net:5655/api/login'
        r = requests.post(url,json={'username': 'filipos', 'password':'Krastavac56'})
        print(json.loads(r.content.decode("utf-8")))
        token = json.loads(r.content.decode("utf-8"))['token']

        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(token)

        # save token for next tests
        with open("token.txt", "w") as file:
            file.write(token)

class TestModelAPI(unittest.TestCase):

    def test_xray(self):
        with open("token.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = 'http://overunderapi.ddns.net:5655/models/xray'
        my_img = {'image': open('test1.jpg', 'rb')}
        headers = {'token': token}
        headers = headers
        r = requests.post(url, files=my_img, headers=headers)
        stream = BytesIO(r.content)
        image = Image.open(stream).convert("RGBA")
        image.save("1.png")
        stream.close()

        self.assertIsNotNone(r.content)
        assert os.path.exists("1.png")
        self.assertEqual(r.status_code, 200)


    def test_coccidia(self):
        url = 'http://overunderapi.ddns.net:5655/models/coccidia'
        my_img = {'image': open('test2.jpg', 'rb')}
        r = requests.post(url, files=my_img)
        stream = BytesIO(r.content)
        image = Image.open(stream).convert("RGBA")
        image.save("2.png")
        stream.close()

        self.assertIsNotNone(r.content)
        assert os.path.exists("2.png")
        self.assertEqual(r.status_code, 200)

    def test_neutrophil(self):
        url = 'http://overunderapi.ddns.net:5655/models/neutrophil'
        my_img = {'image': open('test3.jpg', 'rb')}
        r = requests.post(url, files=my_img)
        stream = BytesIO(r.content)
        image = Image.open(stream).convert("RGBA")
        image.save("3.png")
        stream.close()

        self.assertIsNotNone(r.content)
        assert os.path.exists("3.png")
        self.assertEqual(r.status_code, 200)


