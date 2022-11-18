from datetime import datetime
from adtl.common.utils import encrypt


CREATE_USERS_TABLE = \
    """CREATE TABLE IF NOT EXISTS users 
    (username TEXT PRIMARY KEY,
    password TEXT NOT NULL);
    """

CREATE_POST_TABLE = \
    """CREATE TABLE IF NOT EXISTS post
    (username TEXT NOT NULL,
    post_uid TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    date TEXT NOT NULL,
    tags TEXT,
    FOREIGN KEY (username) REFERENCES users(username));
    """

REGISTER_USER = lambda user: f"INSERT INTO users (username, password) VALUES ('{user.username}', '{user.password}')"

USER_EXISTS = lambda username: f"SELECT * FROM users WHERE username == '{username}'"

USER_AUTH = lambda user: f"SELECT * FROM users WHERE username == '{user.username}' AND password == '{user.password}'"

ADD_POST = lambda post: \
    f"""
    INSERT INTO post (username, post_uid, title, body, date, tags)
    VALUES ('{post.username}', '{encrypt(f"{post.username}{datetime.now()}")}', '{post.title}',
    '{post.body}', '{post.date}', '{post.tags}')
    """

SEARCH_POST_BY_USER = lambda search: \
    f"""
    SELECT * FROM post WHERE username == '{search.username}'
    """

SEARCH_POST_BY_DATE = lambda search: \
    f"""
    SELECT * FROM post WHERE date == '{search.date}'
    """

SEARCH_POST_BY_TITLE = lambda search: \
    f"""
    SELECT * FROM post WHERE title like '%{search.title}%'
    """

SEARCH_POST_BY_BODY = lambda search: \
    f"""
    SELECT * FROM post WHERE body like '%{search.body}%'
    """

SEARCH_POST_BY_TAGS = lambda search: \
    f"""
    SELECT * FROM post WHERE tags like '%{search.tags}%'
    """

DELETE_POST = lambda post_uid: \
    f"""
    DELETE FROM post WHERE post_uid == '{post_uid}'
    """