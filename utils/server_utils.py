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