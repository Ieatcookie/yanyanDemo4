import sys
import db
from json import dumps
from datetime import datetime
import time
import uuid
import re
import hashlib
# from flask_cors import CORS
from flask import Flask, request, jsonify
from db import *
from user_function import *
import os


def register_test():
    db.drop_all()
    db.create_all()
    result = auth_register("nickname", "Phranqueli@gmail.com", "123123", "123123")
    print("111111111", result)
    print("222222222", User.query.all())
    result = auth_register("nickname", "Phranqueli@gmail.com", "123123", "123123")
    print("111111111", result)
    print("222222222", User.query.all())
    result = auth_register("nickname", "1232131@gmail.com", "123123", "123123")
    print("111111111", result)
    print("222222222", User.query.all())
    result = auth_register(
        "nicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenicknamenickname",
        "123213fds1@gmail.com", "123123", "123123")
    print("111111111", result)
    print("222222222", User.query.all())
    result = auth_register("nickname", "1232df131@gmail.com",
                           "123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123",
                           "123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123123")
    print("111111111", result)
    print("222222222", User.query.all())
    result = auth_register("nickname", "12321as31@gmail.com", "123123", "1231234")
    print("111111111", result)
    print("222222222", User.query.all())


def login_test():
    db.drop_all()
    db.create_all()
    result = auth_register("nickname", "Phranqueli@gmail.com", "123123", "123123")
    print("111111111", result)
    print("222222222", User.query.all())
    print(User.query.first().is_online)
    result1 = auth_login("Phranqueli@gmail.com", "123123")
    print(result1 == result)
    print(User.query.first().is_online)

    result1 = auth_login("Phranq@gmail.com", "123123")
    print(result1 == result, result1)

    result1 = auth_login("Phranqueli@gmail.com", "121233123")
    print(result1 == result, result1)


if __name__ == '__main__':
    register_test()
    login_test()
    print(os.path.exists("\\static\\image\\product_image\\1231"))
    print(os.path.exists("static\\image\\product_image\\1231"))

