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
    user = db.session.query(User).filter(User.token==token).first()
    return user

def validate_package(request, db, Package):
    id = request.headers['package-id']
    package_id = Package.query.filter(Package.id == id).with_entities(Package.id).first()
    return package_id