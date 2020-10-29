from secrets import token_urlsafe


def validate_login(request, db, User):
    json = request.get_json()
    user = User.query.filter(User.username == json['username']).first()
    if user.check_password(json['password']):
        token = token_urlsafe(32)
        user.token = token
        db.session.commit()
        db.session().close()
        return token
    else:
        return None


def make_new_user():
    return 2


def validate_token(request, db, User):
    token = request.headers['TOKEN']
    user = db.session.query(User).filter(User.token == token).first()
    return user


def validate_package(request, db, Package):
    id = request.args.get('package-id')
    package_id = Package.query.filter(Package.id == id).with_entities(Package.id).first()
    return package_id


def validate_upload_img_json(json, name):
    if json['name'] is '' or json['name'] is None:
        json['name'] = name
    if json['desc'] is '' or json['desc'] is None:
        json['desc'] = ''
    if json['date'] is '' or json['date'] is None:
        json['date'] = ''
    return json
