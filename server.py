from secrets import token_urlsafe

from PIL import Image
from flask import Flask, request, jsonify, make_response, send_file, Response
from yolov5_server_detect import detect
import os
from flask_sqlalchemy import SQLAlchemy

from models.experimental import attempt_load
app = Flask(__name__)
app.config.from_object("ServerConfig.Config")
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    name = db.Column(db.String(45), unique=False)
    surname = db.Column(db.String(45), unique=False)
    password = db.Column(db.String(45), unique=False)
    thumbnail = db.Column(db.LargeBinary(), unique=False)
    user_role = db.Column(db.Enum('admin','user'), unique=False)
    token = db.Column(db.String(200), unique=False)

    def __init__(self, username, name, surname,password,thumbnail,user_role, token):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.thumbnail = thumbnail
        self.user_role = user_role
        self.token = token

    def __repr__(self):
        return '<User %r>' % self.username



@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        json = request.get_json()
        user = db.session.query(User).filter_by(username=json['username']).first()
        if user.password == json['password']:
            token = token_urlsafe(32)
            user.token = token
            db.session.commit()
            db.session().close()
            response_dict = {'msg':'success', 'token': token}
            return make_response(jsonify(response_dict), 200)
        else:
            return make_response('', 401)

@app.route("/models/xray", methods=["POST"])
def xray_image():
    if request.method == "POST" and request.files:
        token = request.headers['token']
        user = db.session.query(User).filter_by(token=token).first()
        if user.token == token:
            img = Image.open(request.files['image']) # recieve image from post

            path = os.path.join(app.config["XRAY_IMAGE_UPLOADS"], "1.png") # make path for recieved img
            img.save(path, "PNG") # save recieved img
            # detect on received img
            saved_path, predicted_img = detect(model=x_ray_model,source=path,
                                               out=app.config["XRAY_OUTPUT_FOLDER"],
                                               iouThrs=app.config["XRAY_CONF_THRES"],
                                               conf_thres=app.config["XRAY_IOU_THRES"],
                                               agnostic_nms=app.config["XRAY_AGNOSTIC_NMS"],
                                               img_size=512)
            # Remove recieved img
            os.remove(path)
            return send_file(saved_path, mimetype="image/png")
        else:
            return jsonify({'msg': 'fail'})
    else:
        return jsonify({'msg': 'fail'})

@app.route("/models/coccidia", methods=["POST"])
def cocidia_image():
    if request.method == "POST" and request.files:
        img = Image.open(request.files['image']) # recieve image from post
        path = os.path.join(app.config["COCCIDIA_IMAGE_UPLOADS"], "predicted.png") # make path for recieved img
        img.save(path, "PNG") # save recieved img
        # detect on received img
        saved_path, predicted_img = detect(model=coccidia_model, source=path,
                                           out=app.config["COCCIDIA_OUTPUT_FOLDER"],
                                           iouThrs=app.config["COCCIDIA_CONF_THRES"],
                                           conf_thres=app.config["COCCIDIA_IOU_THRES"],
                                           agnostic_nms=app.config["COCCIDIA_AGNOSTIC_NMS"],
                                           img_size=512)
        # Remove recieved img
        os.remove(path)
        return send_file(saved_path, mimetype="image/png")
    else:
        return jsonify({'msg': 'fail'})

@app.route("/models/neutrophil", methods=["POST"])
def neutrophil_image():
    if request.method == "POST" and request.files:
        img = Image.open(request.files['image']) # recieve image from post
        path = os.path.join(app.config["NEUTROPHIL_IMAGE_UPLOADS"], "predicted.png") # make path for recieved img
        img.save(path, "PNG") # save recieved img
        # detect on received img
        saved_path, predicted_img = detect(model=neutrophil_model, source=path,
                                           out=app.config["NEUTROPHIL_OUTPUT_FOLDER"],
                                           iouThrs=app.config["NEUTROPHIL_CONF_THRES"],
                                           conf_thres=app.config["NEUTROPHIL_IOU_THRES"],
                                           agnostic_nms=app.config["NEUTROPHIL_AGNOSTIC_NMS"],
                                           img_size=512, names=['neutrophil'])
        # Remove recieved img
        os.remove(path)
        return send_file(saved_path, mimetype="image/png")
    else:
        return jsonify({'msg': 'fail'})


if __name__ == "__main__":

    x_ray_model = attempt_load(app.config["XRAY_WEIGHTS"], map_location='cuda')  # load FP32 model
    coccidia_model = attempt_load(app.config["COCCIDIA_WEIGHTS"], map_location='cuda')
    neutrophil_model = attempt_load(app.config["NEUTROPHIL_WEIGHTS"], map_location='cuda')


    app.run(debug=True,host="0.0.0.0", port = 5655)


