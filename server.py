from PIL import Image
from flask import Flask, request, jsonify, make_response, send_file
import argparse
import os
import platform
import shutil
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords,
    xyxy2xywh, plot_one_box, strip_optimizer, set_logging)
from utils.torch_utils import select_device, load_classifier, time_synchronized



app = Flask(__name__)
# XRay
app.config["IMAGE_UPLOADS"] = "recievedImgFolder/"
app.config["x_ray_weights"] = "runs/xray_airport_x/exp0_xray_airport_x/weights/best.pt"
app.config["agnostic_nms"] = True
app.config["outputFolderXray"] = "serverOutput/xray"
app.config["xRayConfThres"] = 0.5
app.config["xRayIOUThres"] = 0.5

#Coccidia
app.config["IMAGE_UPLOADS"] = "recievedImgFolder/"
app.config["coccidia_weights"] = "runs/yolom_coccidia/weights/best.pt"
app.config["agnostic_nms"] = True
app.config["outputFolderCoccidia"] = "serverOutput/coccidia"
app.config["coccidiaConfThres"] = 0.8
app.config["coccidiaIOUThres"] = 0.8

#Neutrophil
app.config["IMAGE_UPLOADS"] = "recievedImgFolder/"
app.config["neutrophil_weights"] = "runs/exp1_neutrophils_m_finetune/weights/best.pt"
app.config["agnostic_nms"] = True
app.config["outputFolderNeutrophil"] = "serverOutput/neutrohpil"
app.config["neutrophilConfThres"] = 0.7
app.config["neutrophilIOUThres"] = 0.7

@app.route("/api/xray", methods=["POST"])
def xray_image():
    if request.method == "POST" and request.files:
        img = Image.open(request.files['image']) # recieve image from post
        path = os.path.join(app.config["IMAGE_UPLOADS"], "predicted.png") # make path for recieved img
        img.save(path, "PNG") # save recieved img
        # detect on received img
        saved_path, predicted_img = detect(model=x_ray_model,source=path,
                                           out=app.config["outputFolderXray"],
                                           iouThrs=app.config["xRayConfThres"],
                                           conf_thres=app.config["xRayConfThres"],
                                           img_size=512)
        # Remove recieved img
        os.remove(path)
        return send_file(saved_path, mimetype="image/png")
    else:
        return jsonify({'msg': 'fail'})

@app.route("/api/coccidia", methods=["POST"])
def cocidia_image():
    if request.method == "POST" and request.files:
        img = Image.open(request.files['image']) # recieve image from post
        path = os.path.join(app.config["IMAGE_UPLOADS"], "predicted.png") # make path for recieved img
        img.save(path, "PNG") # save recieved img
        # detect on received img
        saved_path, predicted_img = detect(model=coccidia_model, source=path,
                                           out=app.config["outputFolderNeutrophil"],
                                           iouThrs=app.config["neutrophilConfThres"],
                                           conf_thres=app.config["neutrophilIOUThres"],
                                           img_size=512)
        # Remove recieved img
        os.remove(path)
        return send_file(saved_path, mimetype="image/png")
    else:
        return jsonify({'msg': 'fail'})

@app.route("/api/neutrophil", methods=["POST"])
def neutrophil_image():
    if request.method == "POST" and request.files:
        img = Image.open(request.files['image']) # recieve image from post
        path = os.path.join(app.config["IMAGE_UPLOADS"], "predicted.png") # make path for recieved img
        img.save(path, "PNG") # save recieved img
        # detect on received img
        saved_path, predicted_img = detect(model=neutrophil_model, source=path,
                                           out=app.config["outputFolderCoccidia"],
                                           iouThrs=app.config["coccidiaConfThres"],
                                           conf_thres=app.config["coccidiaIOUThres"],
                                           img_size=512, names=['neutrophil'])
        # Remove recieved img
        os.remove(path)
        return send_file(saved_path, mimetype="image/png")
    else:
        return jsonify({'msg': 'fail'})



def detect(model,source, out, img_size, iouThrs, conf_thres, names=None):

    # Initialize
    set_logging()
    device = select_device('cuda')
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder
    half = device.type != 'cpu'  # half precision only supported on CUDA

    imgsz = check_img_size(img_size, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16
    save_img = True
    dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    if names == None:
        names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]

    # Run inference
    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iouThrs, classes=None, agnostic=app.config["agnostic_nms"] )
        t2 = time_synchronized()

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            p, s, im0 = path, '', im0s

            save_path = str(Path(out) / Path(p).name)
            txt_path = str(Path(out) / Path(p).stem) + ('_%g' % dataset.frame if dataset.mode == 'video' else '')
            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += '%g %ss, ' % (n, names[int(c)])  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_img:  # Add bbox to image
                        label = '%s %.2f' % (names[int(cls)], conf)
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)

            # Print time (inference + NMS)
            print('%sDone. (%.3fs)' % (s, t2 - t1))

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'images':
                    cv2.imwrite(save_path, im0)

    print('Done. (%.3fs)' % (time.time() - t0))
    return save_path, im0

if __name__ == "__main__":
    print("Business Layer Server Started...")

    x_ray_model = attempt_load(app.config["x_ray_weights"], map_location='cuda')  # load FP32 model
    coccidia_model = attempt_load(app.config["coccidia_weights"], map_location='cuda')
    neutrophil_model = attempt_load(app.config["neutrophil_weights"], map_location='cuda')

    app.run(debug=True)