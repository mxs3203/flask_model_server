import glob
import os

def make_recieving_img_name(configFolder):
    if not os.listdir(configFolder):
        name = "1.png"
    else:
        files = os.listdir(configFolder)
        max_num = max([int(str.split(file, sep=".")[0]) for file in files])
        num = max_num + 1
        name = str(num) + ".png"
    return name

def erase_local_files():
    filelist = glob.glob(os.path.join('/home/mateo/Desktop/server/serverOutput/coccidia/', "*"))
    for f in filelist:
        os.remove(f)
    files = glob.glob(os.path.join('/home/mateo/Desktop/server/serverOutput/neutrohpil/', '*'))
    for f in files:
        os.remove(f)
    files = glob.glob(os.path.join('/home/mateo/Desktop/server/serverOutput/xray/', '*'))
    for f in files:
        os.remove(f)

    files = glob.glob(os.path.join('/home/mateo/Desktop/server/recievedImgFolder/xray/','*'))
    for f in files:
        os.remove(f)
    files = glob.glob(os.path.join('/home/mateo/Desktop/server/recievedImgFolder/coccidia/','*'))
    for f in files:
        os.remove(f)
    files = glob.glob(os.path.join('/home/mateo/Desktop/server/recievedImgFolder/neutrohpil/','*'))
    for f in files:
        os.remove(f)