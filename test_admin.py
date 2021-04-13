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
from admin_function import *


def order_test():
    db.drop_all()
    db.create_all()
    token_str = str('1234567'.encode())
    create_user(10000, '1234567', 'nickname', False, "Phranqueli@gmail.com", "123123", "123123", '0405075066')
    create_order(10000, 0, '2021/08/30', 'kingford', 'good', '02020')
    create_order(10000, 0, '2021/08/31', 'zetland', 'soso', '03030')
    print(admin_orders_result(token_str))

def conversion_from_dict():
    db.drop_all()
    db.create_all()
    load_data()
    token_str = str('1234567'.encode())

    create_user(10000, '1234567', 'nickname', False, "Phranqueli@gmail.com", "123123", "123123", '0405075066')
    create_order(10000, 0, '2021/08/31', 'zetland', 'soso', '03030')
    create_op(10001,123)
    create_op(10001,111)
    print(Product.query.filter_by(pro_id = 123).first())
    print(admin_orders_result(token_str))

if __name__ == '__main__':
    order_test()  
    conversion_from_dict()
    db.drop_all()

