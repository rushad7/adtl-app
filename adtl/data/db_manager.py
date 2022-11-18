from enum import Enum

import sqlite3
from sqlite3 import Connection, Cursor
from typing import Optional

import pandas as pd

from adtl.common.logger import ADTLLogger
from adtl.data import query
from adtl.common import DB_NAME
from adtl.data.models import UserModel, PostModel, PostSearchModel


class DatabaseResponseStatus(Enum):
    READ_SUCCESSFUL = {"status": 200, "message": "Successfully read from database"}
    READ_FAILED = {"status": 400, "message": "Failed to read from database"}
    WRITE_SUCCESSFUL = {"status": 200, "message": "Successfully wrote to database"}
    WRITE_FAILED = {"status": 400, "message": "Failed to write to database"}


class DatabaseManager:
    __shared_instance = None

    def __init__(self):
        self.logger = ADTLLogger.get_instance()
        if DatabaseManager.__shared_instance is not None:
            raise Exception("Can instantiate singleton class only once")
        else:
            DatabaseManager.__shared_instance = self
            self.connection = self.__create_connection()
            self.create_user_table()
            self.create_post_table()

    @staticmethod
    def get_instance():
        """Static Access Method"""
        if DatabaseManager.__shared_instance is None:
            DatabaseManager()
        return DatabaseManager.__shared_instance

    @staticmethod
    def __create_connection() -> Connection:
        conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        return conn

    def create_user_table(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute(query.CREATE_USERS_TABLE)
        self.connection.commit()
        cursor.close()

    def create_post_table(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute(query.CREATE_POST_TABLE)
        self.connection.commit()
        cursor.close()

    def register_user(self, user: UserModel) -> DatabaseResponseStatus:
        try:
            cursor = self.connection.cursor()
            cursor.execute(query.REGISTER_USER(user))
            self.connection.commit()
            cursor.close()
            return DatabaseResponseStatus.READ_SUCCESSFUL

        except sqlite3.IntegrityError as e:
            self.logger.error(str(e))
            return DatabaseResponseStatus.READ_FAILED

    def user_exists(self, username: str) -> DatabaseResponseStatus:
        try:

            cursor = self.connection.cursor()
            cursor.execute(query.USER_EXISTS(username))
            row_count = len(cursor.fetchall())
            cursor.close()

            return DatabaseResponseStatus.READ_SUCCESSFUL if row_count == 1 else DatabaseResponseStatus.READ_FAILED

        except Exception as e:
            self.logger.error(str(e))
            return DatabaseResponseStatus.READ_FAILED

    def user_auth(self, user: UserModel) -> DatabaseResponseStatus:
        try:

            cursor = self.connection.cursor()
            cursor.execute(query.USER_AUTH(user))
            row_count = len(cursor.fetchall())
            cursor.close()

            return DatabaseResponseStatus.READ_SUCCESSFUL if row_count == 1 else DatabaseResponseStatus.READ_FAILED

        except Exception as e:
            self.logger.error(str(e))
            return DatabaseResponseStatus.READ_FAILED

    def add_post(self, post: PostModel) -> DatabaseResponseStatus:
        try:
            cursor = self.connection.cursor()
            cursor.execute(query.ADD_POST(post))
            self.connection.commit()
            cursor.close()

            return DatabaseResponseStatus.WRITE_SUCCESSFUL

        except Exception as e:
            self.logger.error(str(e))
            return DatabaseResponseStatus.WRITE_FAILED

    def search_post(self, search_post: PostSearchModel) -> dict:
        try:
            search_query_dict = {"username": query.SEARCH_POST_BY_USER, "date": query.SEARCH_POST_BY_DATE,
                                 "title": query.SEARCH_POST_BY_TITLE, "body": query.SEARCH_POST_BY_BODY,
                                 "tags": query.SEARCH_POST_BY_TAGS}

            final_search_df: Optional[pd.DataFrame] = None
            cursor: Optional[Cursor] = None

            for search_key, search_value in search_post.dict().items():
                if search_value is not None:
                    cursor = self.connection.cursor()
                    cursor.execute(search_query_dict.get(search_key)(search_post))

                    if final_search_df is None:
                        final_search_df = pd.DataFrame(cursor.fetchall())
                    else:
                        temp_df = pd.DataFrame(cursor.fetchall())
                        final_search_df = pd.merge(temp_df, final_search_df, how="inner")

            cursor.close()
            final_search_df.columns = ["username", "post_uid", "title", "body", "date", "tags"]
            return final_search_df.to_dict("index")

        except Exception as e:
            self.logger.error(str(e))

    def delete_post(self, post_uid: str) -> DatabaseResponseStatus:
        try:
            cursor = self.connection.cursor()
            cursor.execute(query.DELETE_POST(post_uid))
            self.connection.commit()
            cursor.close()
            return DatabaseResponseStatus.WRITE_SUCCESSFUL

        except Exception as e:
            self.logger.error(str(e))
            return DatabaseResponseStatus.WRITE_FAILED
