from functools import wraps

from flask_pydantic import validate
from flask import request, session, make_response, jsonify, Blueprint

from adtl.common.utils import encrypt
from adtl.data.db_manager import DatabaseManager
from adtl.data.models import UserModel, StandardResponseModel, PostModel, PostSearchModel, DeletePostModel


app_routes = Blueprint('app_routes', __name__)
db_manager = DatabaseManager()


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not session.get("authorized"):
            return make_response(jsonify(status=401, message="Invalid Authentication"))
        return f(*args, **kwargs)

    return decorator


@app_routes.route("/login", methods=["POST"])
@validate(body=UserModel)
def login():
    # TODO : AUTH
    username = request.json.get("username")
    password_encrypted = encrypt(request.json.get("password"))
    user = UserModel(username=username, password=password_encrypted)

    user_auth_status = db_manager.user_auth(user).value.get("status")

    if user_auth_status == 200:
        session["authorized"] = True
        session["active_user"] = user.username
        return StandardResponseModel(status=200, message="Logged in successfully")

    else:
        session["authorized"] = None
        session["active_user"] = None
        return StandardResponseModel(status=400, message="Incorrect username or password")


@app_routes.route("/register", methods=["POST"])
@validate(body=UserModel)
def register_user():
    username = request.json.get("username")
    password_encrypted = encrypt(request.json.get("password"))
    user = UserModel(username=username, password=password_encrypted)

    if db_manager.user_exists(username).value.get("status"):
        db_manager.register_user(user)
        return jsonify(status=200, message="Registered successfully")

    else:
        return jsonify(status=400, message="Username taken")


@app_routes.route("/add-post", methods=["POST"])
@validate(body=PostModel)
@login_required
def add_post():
    username = session.get("active_user")
    title = request.json.get("title")
    body = request.json.get("body")
    date = request.json.get("date")
    tags = request.json.get("tags")

    post = PostModel(username=username, title=title, body=body, date=date, tags=tags)
    status = db_manager.add_post(post)

    return jsonify(status=status.value.get("status"))


@app_routes.route("/search-post", methods=["POST"])
@validate(body=PostSearchModel)
@login_required
def search_post():
    username = session.get("active_user")
    title = request.json.get("title")
    body = request.json.get("body")
    date = request.json.get("date")
    tags = request.json.get("tags")

    post_search = PostSearchModel(username=username, title=title, body=body, date=date, tags=tags)
    search_result = db_manager.search_post(post_search)

    return jsonify(search_result=search_result)


@app_routes.route("/delete-post", methods=["POST"])
@validate(body=DeletePostModel)
@login_required
def delete_post():
    post_uid = request.json.get("post_uid")
    db_manager.delete_post(post_uid)
    return jsonify(status=200)
