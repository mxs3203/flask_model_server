import os
from secrets import token_urlsafe
from image_slicer import slice
import PIL
from PIL import Image
from flask import Flask, request, jsonify, make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from models.experimental import attempt_load
from sqlalchemy.orm import session
from yolov5_server_detect import detect
from utils.server_utils import make_recieving_img_name

PIL.Image.MAX_IMAGE_PIXELS = 979515483
app = Flask(__name__)
app.config.from_object("ServerConfig.Config")
db = SQLAlchemy(app)

class Img(db.Model):
    __tablename__ = 'img'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    imgpath = db.Column(db.String(200), unique=True)
    small_imgpath = db.Column(db.String(200), unique=True)
    uploaded = db.Column(db.BOOLEAN, unique=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, imgpath, small_imgpath, uploaded, package_id, user_id):
        self.imgpath = imgpath
        self.small_imgpath = small_imgpath
        self.uploaded = uploaded
        self.package_id = package_id
        self.user_id = user_id

    def __repr__(self):
        return '<Img %r>' % self.imgpath
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True )
    username = db.Column(db.String(45), unique=True)
    name = db.Column(db.String(45), unique=False)
    surname = db.Column(db.String(45), unique=False)
    password = db.Column(db.String(45), unique=False)
    thumbnail = db.Column(db.LargeBinary(), unique=False)
    user_role = db.Column(db.Enum('admin', 'user'), unique=False)
    token = db.Column(db.String(200), unique=False)

    def __init__(self, username, name, surname, password, thumbnail, user_role, token):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.thumbnail = thumbnail
        self.user_role = user_role
        self.token = token

    def __repr__(self):
        return '<User %r>' % self.username
class Package_User_Cross(db.Model):
    __tablename__ = 'package_user_cross'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)

    def __init__(self,id, user_id, package_id):
        self.id = id
        self.user_id = user_id
        self.package_id = package_id

    def __repr__(self):
        return '<Cross ID %r>' % self.id
class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    name = db.Column(db.String(45), nullable=False)

    def __init__(self,id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Package %r>' % self.name


@app.route("/api/getallusers", methods=["GET"])
def getallusers():
    if request.method == "GET":
        token = request.headers['token']
        results = User.query.filter(User.token == token).first()

        if results is not None and results.user_role == 'admin':
            results = User.query.join(Package_User_Cross).join(Package).add_columns(Package.name).all()
            output = {}
            packages = []
            for result in results:
                packages.append(result[1])
                if output.keys().__contains__(result[0].username):
                    packages = []
                else:
                    output[result[0].username] = {'username': result[0].username, 'name': result[0].name,
                                              'surname': result[0].surname, 'user_role': result[0].user_role,
                                              'packages': packages}


            return make_response(output, 200)
        else:
            return make_response('{}', 401)


@app.route("/api/getallimages", methods=["GET"])
def getallimages():
    if request.method == "GET":
        token = request.headers['token']
        package = request.headers['package']
        user = User.query.filter(User.token == token).first()
        package_model = Package.query.filter(Package.name == package).first()

        if user is not None and package_model is not None:
            results_uploaded = User.query.filter(User.id == user.id).join(Img).join(Package).filter(Package.id == package_model.id).add_columns(Img.imgpath, Img.uploaded).filter(Img.uploaded == True).all()
            results_generated = User.query.filter(User.id == user.id).join(Img).join(Package).filter(Package.id == package_model.id).add_columns(Img.imgpath, Img.uploaded).filter(Img.uploaded == False).all()

            output = {}
            cnt = 0
            uploaded = []
            generated = []
            for res in results_uploaded:
                generated.append(results_generated[cnt][1])
                uploaded.append(res[1])
                cnt = cnt + 1
            output['generated'] = generated
            output['uploaded'] = uploaded
            return make_response(output, 200)
        else:
            return make_response('{}', 401)


@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        json = request.get_json()
        result = User.query.filter(User.username==json['username']).join(Package_User_Cross).join(Package).add_columns(Package.name).all()
        user = result[0][0]
        packages = [res[1] for res in result]
        if user.password == json['password']:
            token = token_urlsafe(32)
            user.token = token
            role = user.user_role
            db.session.commit()
            db.session().close()
            response_dict = {'msg': 'success', 'token': token, 'user_role': role, 'packages': packages}
            return make_response(jsonify(response_dict), 200)
        else:
            return make_response('{}', 401)
    return make_response('{}', 404)

@app.route("/models/xray", methods=["POST"])
def xray_image():
    if request.method == "POST" and request.files:
        token = request.headers['token']
        package = request.headers['package']
        package_id = Package.query.filter(Package.name==package).with_entities(Package.id).first()
        user = db.session.query(User).filter_by(token=token).first()

        if user is not None and package_id is not None and user.token == token:
            package_id = package_id[0]
            img = Image.open(request.files['image'])  # recieve image from post
            name = make_recieving_img_name(app.config["XRAY_IMAGE_UPLOADS"])
            path = os.path.join(app.config["XRAY_IMAGE_UPLOADS"], name)  # make path for recieved img
            img.save(path, "PNG")  # save recieved img

            # detect on received img
            saved_path = detect(model=x_ray_model, source=path,
                                               out=app.config["XRAY_OUTPUT_FOLDER"],
                                               iouThrs=app.config["XRAY_CONF_THRES"],
                                               conf_thres=app.config["XRAY_IOU_THRES"],
                                               agnostic_nms=app.config["XRAY_AGNOSTIC_NMS"],
                                               img_size=app.config["XRAY_IMG_SIZE"])

            img_db = Img(imgpath=path, small_imgpath=path,uploaded=True,package_id=package_id,user_id=user.id)
            db.session.add(img_db)
            img_db = Img(imgpath=saved_path, small_imgpath=saved_path, uploaded=False, package_id=package_id,user_id=user.id)
            db.session.add(img_db)
            db.session.commit()

            return jsonify({'msg': 'success', 'img_path':saved_path})
        else:
            return make_response('{}', 401)
    else:
        return jsonify({'msg': 'fail'})


@app.route("/models/coccidia", methods=["POST"])
def cocidia_image():
    if request.method == "POST" and request.files:
        token = request.headers['token']
        package = request.headers['package']
        package_id = Package.query.filter(Package.name == package).with_entities(Package.id).first()
        user = db.session.query(User).filter_by(token=token).first()
        if user is not None and package_id is not None and user.token == token:
            img = Image.open(request.files['image'])  # recieve image from post
            name = make_recieving_img_name(app.config["XRAY_IMAGE_UPLOADS"])
            path = os.path.join(app.config["COCCIDIA_IMAGE_UPLOADS"], name)  # make path for recieved img
            img.save(path, "PNG")  # save recieved img

            # detect on received img
            saved_path = detect(model=coccidia_model, source=path,
                                               out=app.config["COCCIDIA_OUTPUT_FOLDER"],
                                               iouThrs=app.config["COCCIDIA_CONF_THRES"],
                                               conf_thres=app.config["COCCIDIA_IOU_THRES"],
                                               agnostic_nms=app.config["COCCIDIA_AGNOSTIC_NMS"],
                                               img_size=app.config["COCCIDIA_IMG_SIZE"])
            img_db = Img(imgpath=path, small_imgpath=path, uploaded=True, package_id=package_id, user_id=user.id)
            db.session.add(img_db)
            img_db = Img(imgpath=saved_path, small_imgpath=saved_path, uploaded=False, package_id=package_id,
                         user_id=user.id)
            db.session.add(img_db)
            db.session.commit()

            return jsonify({'msg': 'success', 'img_path':saved_path})
        else:
            return make_response('{}', 401)
    else:
        return jsonify({'msg': 'fail'})


@app.route("/models/neutrophil", methods=["POST"])
def neutrophil_image():
    if request.method == "POST" and request.files:
        img = Image.open(request.files['image'])  # recieve image from post
        path = os.path.join(app.config["NEUTROPHIL_IMAGE_UPLOADS"], "predicted.png")  # make path for recieved img
        img.save(path, "PNG")  # save recieved img
        # detect on received img
        saved_path = detect(model=neutrophil_model, source=path,
                                           out=app.config["NEUTROPHIL_OUTPUT_FOLDER"],
                                           iouThrs=app.config["NEUTROPHIL_CONF_THRES"],
                                           conf_thres=app.config["NEUTROPHIL_IOU_THRES"],
                                           agnostic_nms=app.config["NEUTROPHIL_AGNOSTIC_NMS"],
                                           img_size=app.config["NEUTROPHIL_IMG_SIZE"], names=['neutrophil'])

        return send_file(saved_path, mimetype="image/png")
    else:
        return jsonify({'msg': 'fail'})


if __name__ == "__main__":
    x_ray_model = attempt_load(app.config["XRAY_WEIGHTS"], map_location='cuda')  # load FP32 model
    coccidia_model = attempt_load(app.config["COCCIDIA_WEIGHTS"], map_location='cuda')
    neutrophil_model = attempt_load(app.config["NEUTROPHIL_WEIGHTS"], map_location='cuda')

    app.run(debug=True, host="0.0.0.0", port=5655)
