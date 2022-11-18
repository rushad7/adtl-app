from typing import Optional
from pydantic import BaseModel, constr


class StandardResponseModel(BaseModel):
    status: int
    message: Optional[str]


class UserModel(BaseModel):
    username: str
    password: constr(min_length=7)


class PostModel(BaseModel):
    username: Optional[str]
    title: str
    date: str
    body: str
    tags: Optional[str]


class PostSearchModel(BaseModel):
    username: Optional[str]
    title: Optional[str]
    date: Optional[str]
    body: Optional[str]
    tags: Optional[str]


class DeletePostModel(BaseModel):
    post_uid: str
