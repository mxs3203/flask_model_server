import glob
import os
from secrets import token_urlsafe


def make_recieving_img_name(configFolder):
    if not os.listdir(configFolder):
        name = "1.png"
    else:
        files = os.listdir(configFolder)
        max_num = max([int(str.split(file, sep=".")[0]) for file in files])
        num = max_num + 1
        name = str(num) + ".png"
    return name

def make_new_user(user, json,db, User):
    if user.user_role == 'admin':
        if json is not None:
            token = token_urlsafe(32)
            newuser = User(token=token, password=json['password'], name=json['name'], username=json['username'],
                           surname=json['username'], thumbnail=None, user_role=json['user_role'])
            db.session.add(newuser)
            db.session.commit()
            db.session.close()
            return 200, token
        else:
            return 404, None
    else:
        return 401, None

def delete_user(user, json,db, User):
    if user.user_role == 'admin':
        if json is not None and json['username'] is not None:
            User.query.filter(User.username == json['username']).delete()
            db.session.commit()
            db.session.close()
            return 200
        return 404
    else:
        return 401


def erase_local_files():
    filelist = glob.glob(os.path.join('/home/mateo/Desktop/server/images/serverOutput/coccidia/', "*"))
    for f in filelist:
        print(f)
        os.remove(f)
    files = glob.glob(os.path.join('/home/mateo/Desktop/server/images/serverOutput/neutrohpil/', '*'))
    for f in files:
        os.remove(f)
    files = glob.glob(os.path.join('/home/mateo/Desktop/server/images/serverOutput/xray/', '*'))
    for f in files:
        os.remove(f)


    files = glob.glob(os.path.join('/home/mateo/Desktop/server/images/recievedImgFolder/xray/', '*'))
    for f in files:
        os.remove(f)
    files = glob.glob(os.path.join('/home/mateo/Desktop/server/images/recievedImgFolder/coccidia/', '*'))
    for f in files:
        os.remove(f)
    files = glob.glob(os.path.join('/home/mateo/Desktop/server/images/recievedImgFolder/neutrohpil/', '*'))
    for f in files:
        os.remove(f)