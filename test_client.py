from io import BytesIO
import json

import PIL
import requests
from PIL import Image
import os
import unittest
PIL.Image.MAX_IMAGE_PIXELS = 979515483

URL = 'http://overunderapi.ddns.net:5655'

class Test1_LoginAPI(unittest.TestCase):
    print("LOGIN TESTS Started")
    def test_incorrect_login(self):
        print("TEST: Incorrect LOGIN :")
        url = URL + '/api/login'
        r = requests.post(url, json={'username': 'filipos', 'password':'krivipass'})
        self.assertEqual(r.status_code, 401)
        print("TEST END: Incorrect LOGIN :")

    def test_correct_login_admin(self):
        print("TEST: Correct LOGIN admin:")
        url = URL + '/api/login'
        r = requests.post(url, json={'username': 'filipos', 'password':'Krastavac56'})
        jsonObj = json.loads(r.content.decode("utf-8"))
        token = jsonObj['token']

        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(token)
        # save token for next tests
        with open("token_admin.txt", "w") as file:
            file.write(token)
        print("TEST END: Correct LOGIN admin:")

    def test_correct_login_user(self):
        print("TEST: Correct LOGIN :")
        url = URL + '/api/login'
        r = requests.post(url,json={'username': 'ihor', 'password':'Krastavac56'})
        jsonObj = json.loads(r.content.decode("utf-8"))
        token = jsonObj['token']

        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(token)

        # save token for next tests
        with open("token_user.txt", "w") as file:
            file.write(token)
        print("TEST END: Correct LOGIN :")

    def test_get_user_account(self):
        print("TEST: Get user account:")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/user-account'
        headers = {'token': token}
        r = requests.get(url, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        print(jsonObj)
        self.assertIsNotNone(jsonObj)
        self.assertEqual(r.status_code, 200)
        print("TEST END: Get user account:")

class Test2_ModelAPI(unittest.TestCase):
    print("MODEL API TESTS Started")
    def test_xray(self):
        print("TEST XRAY Model")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/models/xray'
        img_file = open('test1.jpg', 'rb')
        my_img = {'image': img_file}
        headers = {'token': token, 'package-id':'2'}
        r = requests.post(url, files=my_img, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        img_file.close()

        self.assertIsNotNone(jsonObj)
        self.assertIsNotNone(jsonObj['img_path'])
        assert os.listdir("/home/mateo/Desktop/server/recievedImgFolder/xray/")
        assert os.listdir("/home/mateo/Desktop/server/serverOutput/xray/")
        self.assertEqual(r.status_code, 200)

        print("TEST END: XRAY Model")

    def test_xray_wrong_token(self):
        print("TEST: XRAY Model wrong token")
        token = "wrongtoken1294uhjnmds"
        url = URL + '/models/xray'
        img_file = open('test1.jpg', 'rb')
        my_img = {'image': img_file}
        headers = {'token': token, 'package-id': '2'}
        r = requests.post(url, files=my_img, headers=headers)
        img_file.close()

        self.assertEqual(r.status_code, 401)
        print("TEST END: XRAY Model wrong token")

    def test_xray_wrong_package(self):
        print("TEST END: XRAY Model wrong package id")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/models/xray'
        img_file = open('test1.jpg', 'rb')
        my_img = {'image': img_file}
        headers = {'token': token, 'package-id': 'jkgasjh'}
        r = requests.post(url, files=my_img, headers=headers)
        img_file.close()

        self.assertEqual(r.status_code, 401)
        print("TEST END: XRAY Model wrong package id")

    def test_coccidia(self):
        print("TEST: Coccidia Model")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/models/coccidia'
        img_file = open('test2.jpg', 'rb')
        my_img = {'image': img_file}
        headers = {'token': token, 'package-id': '1'}
        r = requests.post(url, files=my_img, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        img_file.close()

        self.assertIsNotNone(jsonObj)
        self.assertIsNotNone(jsonObj['img_path'])
        assert os.listdir("/home/mateo/Desktop/server/recievedImgFolder/coccidia/")
        assert os.listdir("/home/mateo/Desktop/server/serverOutput/coccidia/")
        self.assertEqual(r.status_code, 200)
        print("TEST END: Coccidia Model")

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
class Test3_APIEndpoints(unittest.TestCase):
    print("Test API Endpoints Started")

    def test_get_all_users_admin(self):
        print("TEST: GET ALL USERS")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/getallusers'
        headers = {'token': token}
        r = requests.get(url, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        print(jsonObj)
        #self.assertEqual(jsonObj, "{'0': {'packages': ['Imaging', 'Finance', 'Sports'], 'username': 'filipos'}, '1': {'packages': ['Finance', 'Sports'], 'username': 'mateo'}}")
        self.assertEqual(r.status_code, 200)
        print("TEST END: GET ALL USERS")

    def test_get_all_users_user(self):
        print("TEST: GET ALL USERS-user role")
        with open("token_user.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/getallusers'
        headers = {'token': token}
        r = requests.get(url, headers=headers)
        self.assertEqual(r.status_code, 401)
        print("TEST END: GET ALL USERS-user role")

    def test_get_all_images(self):
        print("TEST: GET ALL IMAGES")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/getallimages'
        headers = {'token': token, 'package-id': '1'}
        r = requests.get(url, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        print(jsonObj)
        self.assertNotEqual(jsonObj['generated'], [])
        self.assertNotEqual(jsonObj['uploaded'], [])
        self.assertEqual(r.status_code, 200)
        print("TEST END: GET ALL IMAGES")

    def test_get_all_images_no_images(self):
        print("TEST: GET ALL IMAGES - no images")
        with open("token_user.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/getallimages'
        headers = {'token': token, 'package-id': '2'}
        r = requests.get(url, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        print(jsonObj)
        self.assertEqual(jsonObj['generated'], [])
        self.assertEqual(jsonObj['uploaded'], [])
        self.assertEqual(r.status_code, 200)
        print("TEST END: GET ALL IMAGES - no images")

class Test4_erase(unittest.TestCase):
    print('Erasing all...')
    def test_erase_local_files(self):

        url = URL + '/api/eraseLocal'
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = None
    unittest.main(testLoader=loader)
