import json

import PIL
import requests
from PIL import Image
import unittest
PIL.Image.MAX_IMAGE_PIXELS = 979515483

URL = 'http://overunderapi.ddns.net:5655'

class Test1_LoginAPI(unittest.TestCase):
    print("LOGIN TESTS Started")
    def test_incorrect_login(self):
        print("TEST: Incorrect LOGIN :")
        url = URL + '/api/login'
        r = requests.post(url, json={'username': 'mateo', 'password':'krivipass'})
        self.assertEqual(r.status_code, 401)
        print("TEST END: Incorrect LOGIN :\n")

    def test_correct_login_admin(self):
        print("TEST: Correct LOGIN admin:")
        url = URL + '/api/login'
        r = requests.post(url, json={'username': 'mateo', 'password':'Krastavac56'})
        jsonObj = json.loads(r.content.decode("utf-8"))
        token = jsonObj['token']

        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(token)
        # save token for next tests
        with open("token_admin.txt", "w") as file:
            file.write(token)
        print("TEST END: Correct LOGIN admin: \n")

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
        print("TEST END: Correct LOGIN :\n")

    def test_get_user_account(self):
        print("TEST: Get user account:")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/user-account'
        headers = {'TOKEN': token}
        r = requests.get(url, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        print(jsonObj)
        self.assertIsNotNone(jsonObj)
        self.assertEqual(r.status_code, 200)
        print("TEST END: Get user account:\n")
class Test2_ModelAPI(unittest.TestCase):
    print("MODEL API TESTS Started")
    def test_xray(self):
        print("TEST XRAY Model")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/models/xray?package-id=2'
        img_file = open('test1.jpg', 'rb')
        headers = {'TOKEN': token}
        data = {'desc': ' vidi kako je ova slikda dobra', 'name': 'Lepo ko Greh xray ', 'date': '2/12/2011'}
        files = [
            ('image', ('test1.jpg', img_file, 'application/octet')),
            ('json', ('json', json.dumps(data), 'application/json')),
        ]
        r = requests.post(url, files=files, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        img_file.close()

        self.assertIsNotNone(jsonObj)
        self.assertIsNotNone(jsonObj['img_path'])
        self.assertEqual(r.status_code, 200)

        print("TEST END: XRAY Model\n")

    def test_xray_no_name(self):
        print("TEST XRAY Model")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/models/xray?package-id=2'
        img_file = open('test1.jpg', 'rb')
        headers = {'TOKEN': token}
        data = {'desc': '', 'name': '', 'date': '2/12/2011'}
        files = [
            ('image', ('test1.jpg', img_file, 'application/octet')),
            ('json', ('json', json.dumps(data), 'application/json')),
        ]
        r = requests.post(url, files=files, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        img_file.close()

        self.assertIsNotNone(jsonObj)
        self.assertIsNotNone(jsonObj['img_path'])
        self.assertEqual(r.status_code, 200)

        print("TEST END: XRAY Model\n")

    def test_xray_with_none(self):
        print("TEST XRAY Model")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/models/xray?package-id=2'
        img_file = open('test1.jpg', 'rb')
        headers = {'TOKEN': token}
        data = {'desc': None, 'name': None, 'date': None}
        files = [
            ('image', ('test1.jpg', img_file, 'application/octet')),
            ('json', ('json', json.dumps(data), 'application/json')),
        ]
        r = requests.post(url, files=files, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        img_file.close()

        self.assertIsNotNone(jsonObj)
        self.assertIsNotNone(jsonObj['img_path'])
        self.assertEqual(r.status_code, 200)

        print("TEST END: XRAY Model\n")

    def test_xray_wrong_token(self):
        print("TEST: XRAY Model wrong token")
        token = "wrongtoken1294uhjnmds"
        url = URL + '/api/models/xray?package-id=2'
        img_file = open('test1.jpg', 'rb')
        headers = {'TOKEN': token}
        data = {'desc': ' alo bre dobra slika', 'name': 'Lepo ko Greh xray ', 'date': '1/12/2020'}
        files = [
            ('image', ('test1.jpg', img_file, 'application/octet')),
            ('json', ('json', json.dumps(data), 'application/json')),
        ]
        r = requests.post(url, files=files, headers=headers)
        img_file.close()

        self.assertEqual(r.status_code, 401)
        print("TEST END: XRAY Model wrong token\n")

    def test_xray_wrong_package(self):
        print("TEST END: XRAY Model wrong package id")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/models/xray?package-id=dfs'
        img_file = open('test1.jpg', 'rb')
        headers = {'TOKEN': token}
        data = {'desc': ' alo bre dobra slika', 'name': 'Lepo ko Greh xray ', 'date': '1/12/2020'}
        files = [
            ('image', ('test1.jpg', img_file, 'application/octet')),
            ('json', ('json', json.dumps(data), 'application/json')),
        ]
        r = requests.post(url, files=files, headers=headers)
        img_file.close()

        self.assertEqual(r.status_code, 401)
        print("TEST END: XRAY Model wrong package id\n")

    def test_coccidia(self):
        print("TEST: Coccidia Model")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/models/coccidia?package-id=1'
        img_file = open('test2.jpg', 'rb')
        #my_img = {'image': img_file}
        data = {'desc': ' ovo je mnogo lepa slika. ', 'name': 'Lepo ko Greh', 'date':'1/1/2020'}
        headers = {'TOKEN': token}
        files = [
            ('image', ('test2.jpg', img_file, 'application/octet')),
            ('json', ('json', json.dumps(data), 'application/json')),
        ]

        r = requests.post(url, files=files, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        img_file.close()

        self.assertIsNotNone(jsonObj)
        self.assertIsNotNone(jsonObj['img_path'])

        self.assertEqual(r.status_code, 200)
        print("TEST END: Coccidia Model\n")

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
        headers = {'TOKEN': token}
        r = requests.get(url, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        print(jsonObj)
        #self.assertEqual(jsonObj, "{'0': {'packages': ['Imaging', 'Finance', 'Sports'], 'username': 'filipos'}, '1': {'packages': ['Finance', 'Sports'], 'username': 'mateo'}}")
        self.assertEqual(r.status_code, 200)
        print("TEST END: GET ALL USERS\n")

    def test_get_all_users_user(self):
        print("TEST: GET ALL USERS-user role")
        with open("token_user.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/getallusers'
        headers = {'TOKEN': token}
        r = requests.get(url, headers=headers)
        self.assertEqual(r.status_code, 401)
        print("TEST END: GET ALL USERS-user role\n")

    def test_get_all_images_coccidia(self):
        print("TEST: GET ALL IMAGES - coccidia")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/getallimages?package-id=1'
        headers = {'TOKEN': token}
        r = requests.get(url, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        print(jsonObj)
        self.assertIsNotNone(jsonObj)
        self.assertEqual(r.status_code, 200)
        print("TEST END: GET ALL IMAGES - coccidia\n")

    def test_get_all_images_xray(self):
        print("TEST: GET ALL IMAGES - xray")
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/getallimages?package-id=2'
        headers = {'TOKEN': token}
        r = requests.get(url, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        print(jsonObj)
        self.assertIsNotNone(jsonObj)
        self.assertEqual(r.status_code, 200)
        print("TEST END: GET ALL IMAGES - xray\n")

    def test_get_all_images_no_images(self):
        print("TEST: GET ALL IMAGES - no images")
        with open("token_user.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        url = URL + '/api/getallimages?package-id=2'
        headers = {'TOKEN': token}
        r = requests.get(url, headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        print(jsonObj)
        self.assertIsNotNone(jsonObj)
        self.assertEqual(r.status_code, 200)
        print("TEST END: GET ALL IMAGES - no images\n")
class Test5_MakeNewUser(unittest.TestCase):
    print("Test Make New User Started")

    def test0_make_new_user(self):
        print("TEST: Make new user")
        url = URL + '/api/makenewuser'
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        headers = {'TOKEN': token}
        r = requests.post(url,
                          json={'username': 'test@test.com', 'password':'Krastavac56', 'name': 'TestName', 'surname': 'TestSurname', 'user_role': 'user'},
                          headers=headers)
        jsonObj = json.loads(r.content.decode("utf-8"))
        print(jsonObj)
        self.assertEqual(r.status_code, 200)
        print("TEST END: Make new user\n")

    def test1_make_new_user_user_role(self):
        print("TEST: Make new user - user role")
        url = URL + '/api/makenewuser'
        with open("token_user.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        headers = {'TOKEN': token}
        r = requests.post(url,
                          json={'username': 'test@test.com', 'password':'Krastavac56', 'name': 'TestName', 'surname': 'TestSurname', 'user_role': 'user'},
                          headers=headers)
        self.assertEqual(r.status_code, 401)
        print("TEST END: Make new user - user role\n")

    def test2_delete_user(self):
        print("TEST: Delete user")
        url = URL + '/api/deleteuser'
        with open("token_admin.txt", "r") as file:
            token = file.readlines()
        token = token[0]
        headers = {'TOKEN': token}
        r = requests.post(url,
                          json={'username': 'test@test.com'},
                          headers=headers)
        self.assertEqual(r.status_code, 200)
        print("TEST END: Delete User\n")


class Test9_erase(unittest.TestCase):
    print('Erasing all...')
    def test_erase_local_files(self):
        url = URL + '/api/eraseLocal'
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)

if __name__ == '__main__':
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = None
    unittest.main(testLoader=loader)
