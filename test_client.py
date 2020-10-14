from io import BytesIO
import json

import PIL
import requests
from PIL import Image
import os
import unittest

PIL.Image.MAX_IMAGE_PIXELS = 979515483

URL = 'http://overunderapi.ddns.net:5655'

class TestLoginAPI(unittest.TestCase):
    def test_incorrect_login(self):
        url = URL + '/api/login'
        r = requests.post(url,json={'username': 'filipos', 'password':'krivipass'})
        self.assertEqual(r.status_code, 401)

    def test_correct_login_admin(self):
        url = URL + '/api/login'
        r = requests.post(url,json={'username': 'filipos', 'password':'Krastavac56'})
        jsonObj = json.loads(r.content.decode("utf-8"))
        token = jsonObj['token']
        role = jsonObj['user_role']
        packages = jsonObj['packages']

        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(token)
        self.assertIsNotNone(packages)
        self.assertIsNotNone(role)
        assert role == 'admin'
        assert packages == ['Imaging', 'Finance', 'Sports']

        # save token for next tests
        with open("token_admin.txt", "w") as file:
            file.write(token)

    def test_correct_login_user(self):
        url = URL + '/api/login'
        r = requests.post(url,json={'username': 'ihor', 'password':'Krastavac56'})
        jsonObj = json.loads(r.content.decode("utf-8"))
        token = jsonObj['token']
        role = jsonObj['user_role']
        packages = jsonObj['packages']

        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(token)
        self.assertIsNotNone(role)
        assert role == 'user'
        assert packages == ['Imaging']

        # save token for next tests
        with open("token_user.txt", "w") as file:
            file.write(token)

class TestModelAPI(unittest.TestCase):

    def test_xray(self):
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/models/xray'
        img_file = open('test1.jpg', 'rb')
        my_img = {'image': img_file}
        headers = {'token': token, 'package':'Imaging'}
        r = requests.post(url, files=my_img, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        img_file.close()

        self.assertIsNotNone(jsonObj)
        self.assertIsNotNone(jsonObj['img_path'])
        assert os.listdir("recievedImgFolder/xray/")
        assert os.listdir("serverOutput/xray/")
        self.assertEqual(r.status_code, 200)

    def test_xray_wrong_token(self):
        token = "wrongtoken1294uhjnmds"
        url = URL + '/models/xray'
        img_file = open('test1.jpg', 'rb')
        my_img = {'image': img_file}
        headers = {'token': token, 'package': 'Imaging'}
        r = requests.post(url, files=my_img, headers=headers)
        img_file.close()

        self.assertEqual(r.status_code, 401)

    def test_xray_wrong_package(self):
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/models/xray'
        img_file = open('test1.jpg', 'rb')
        my_img = {'image': img_file}
        headers = {'token': token, 'package': 'jkgasjh'}
        r = requests.post(url, files=my_img, headers=headers)
        img_file.close()

        self.assertEqual(r.status_code, 401)

    def test_coccidia(self):
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/models/coccidia'
        img_file = open('test2.jpg', 'rb')
        my_img = {'image': img_file}
        headers = {'token': token, 'package': 'Imaging'}
        r = requests.post(url, files=my_img, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        img_file.close()

        self.assertIsNotNone(jsonObj)
        self.assertIsNotNone(jsonObj['img_path'])
        assert os.listdir("recievedImgFolder/coccidia/")
        assert os.listdir("serverOutput/coccidia/")
        self.assertEqual(r.status_code, 200)

    # def test_neutrophil(self):
    #     url = URL + '/models/neutrophil'
    #     img_file = open('test3.jpg', 'rb')
    #     my_img = {'image': img_file}
    #     r = requests.post(url, files=my_img)
    #     stream = BytesIO(r.content)
    #     image = Image.open(stream).convert("RGBA")
    #     image.save("3.png")
    #     stream.close()
    #     img_file.close()
    #
    #     self.assertIsNotNone(r.content)
    #     assert os.path.exists("3.png")
    #     self.assertEqual(r.status_code, 200)

    # def test_neutrophil_1gb_img(self):
    #     url = URL + '/models/neutrophil'
    #     img_file = open('big_img1.png', 'rb')
    #     my_img = {'image': img_file}
    #     r = requests.post(url, files=my_img)
    #     stream = BytesIO(r.content)
    #     image = Image.open(stream).convert("RGBA")
    #     image.save("4.png")
    #     stream.close()
    #     img_file.close()
    #
    #     self.assertIsNotNone(r.content)
    #     assert os.path.exists("4.png")
    #     self.assertEqual(r.status_code, 200)


