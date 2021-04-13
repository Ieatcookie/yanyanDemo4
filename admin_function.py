import sys
from json import dumps
from datetime import datetime
import time
import uuid
import re
import hashlib
import random
from os import path, mkdir, remove
# from flask_cors import CORS
from flask import Flask, request, jsonify
from db import *
import jwt

def encode(data):
    return jwt.encode(data, "fivebluepetals", algorithm="HS256")


def decode(data):
    return jwt.decode(data, "fivebluepetals", algorithms=["HS256"])


# admin login
def adminLogin(email, password):
    print(email, password)
    if re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email.lower()):
        if email != "1234567@q.com":
            return json.dumps({"result": "ERROR", "reason": "Non-exist email"})
        if password == "1234567":
            return json.dumps({"token": encode({"id": 1})})
        return json.dumps({"result": "ERROR", "reason": "Wrong password"})
    return json.dumps({"result": "ERROR", "reason": "Invalid email"})


# let admin see orders
def admin_orders_result(token_str):
    if decode(token_str)['id'] != 1:
        return dumps({"result": "ERROR", "reason": "user with token is not an admin"})
    else:
        orders = Order.query.all()
        return_list = []
        i = 0
        for order in orders:
            return_list.append(order_to_dict(order))
        return dumps({"orders": return_list})


# let admin see orders
def admin_products_result(token_str):
    if decode(token_str)['id'] != 1:
        return dumps({"result": "ERROR", "reason": "user with token is not an admin"})
    else:
        products = Product.query.order_by(Product.pro_id).all()
        #print("11111", products)
        result = {"products": products}
        prods = [product_to_dict(i) for i in products]
        #print(prods[0])
        return dumps({"products": prods})


def find_prods(IDs):
    list_of_id = IDs.split(";")
    prods = []
    # print(IDs)
    for ID in list_of_id:
        product = getProductById(ID)
        if product is None:
            return dumps({"result": "ERROR", "reason": "id " + ID + " doesn't exist"})
        else:
            prods.append(product_to_dict(product))
    return dumps({"products": prods})


def update_product(token, productId, newTitle, newDescription, newPrice, newQuantity, newcategory, newDiscount, images):
    if  decode(token)['id'] != 1:
        return dumps({"result": "ERROR", "reason": "user with token is not an admin"})
    if len(newTitle) > 50 or len(newTitle) == 0:
        return dumps({"result": "ERROR", "reason": "newTitle should be between 1-1000 characters"})
    if len(newDescription) > 1000 or len(newDescription) == 0:
        return dumps({"result": "ERROR", "reason": "desciption should be between 1-1000 characters"})
    if newPrice < 0:
        return dumps({"result": "ERROR", "reason": "price need to be positive"})
    if newQuantity < 0:
        return dumps({"result": "ERROR", "reason": "quantity need to be positive"})
    if newDiscount < 0:
        return dumps({"result": "ERROR", "reason": "discount need to be positive"})
        #if id  ==  -1 then we are adding new product without any images
    if int(productId) == -1:
        create_product(len(Product.query.all()), newTitle, True, newPrice, newQuantity,
                       round(random.uniform(2, 4) * random.uniform(1, 2) * 100), newDiscount, newcategory, newDescription)
        return {"result": "created success"}
    else:
        product = Product.query.filter_by(pro_id=int(productId)).first()
        if product is None:
            return dumps({"result": "ERROR", "reason": "id " + productId + " doesn't exist"})

        #if there is less image than before , we will delete the reluctant image
        image_links = images.split(',')
        prod_pics = Product_picture.query.filter_by(pro_id = int(productId)).all()
        for prod_pic in prod_pics:
            if prod_pic.pic_link not in image_links:
                remove(prod_pic.pic_link)
                db.session.delete(prod_pic)
                db.session.commit()
        product.name = newTitle
        product.price = newPrice
        product.stock = newQuantity
        product.tags = newcategory
        product.description = newDescription
        product.discount = newDiscount
        db.session.commit()
    return {"result": "updated success"}


def update_order(token, orderid, status, tracknumber):
    if token != str('1234567'.encode()):
        return dumps({"result": "ERROR", "reason": "user with token is not an admin"})
    if status != "cancel" or status != "ship":
        return dumps({"result": "ERROR", "reason": "status code dose not exist"})
    order = Order.query.filter_by(id=int(orderid)).first()
    if order is None:
        return dumps({"result": "ERROR", "reason": "id " + orderid + " doesn't exist"})
    order.status = status
    order.track_number = tracknumber
    db.session.commit()
    return {"result": "success"}


def find_user_by_token(tk):
    user = User.query.filter_by(token=tk).first()
    if user is None:
        return dumps({"result": "ERROR", "reason": "customer with token(" + tk + ") doesn't exist"})
    return dumps(user_to_dict(user))

#save image into folder with name "static\\image\\product_image\\input id"
def save_image_by_id(token, image, Id):
    if  decode(token)['id'] != 1:
        return dumps({"result": "ERROR", "reason": "user with token is not an admin"})
    prod = Product.query.filter_by(pro_id = int(Id)).first()
    if prod is None:
        return dumps({"result": "ERROR", "reason": "id " + Id + " doesn't exist"})
    if(path.exists("static/image/product_image") == False):
        return dumps({"result": "ERROR", "reason": "folder : static/image/product_image" " doesn't exist"})
    image_path = "static/image/product_image/" + Id
    if path.exists(image_path) == False:
        mkdir(image_path)
    i = 0
    while path.exists(image_path + "/" + str(i) + ".jpg"):
        i = i + 1
    image_name = image_path + "/" + str(i) + ".jpg"
    with open(image_name,"wb") as f:
        f.write(image)
    create_product_picture(image_name, int(Id))
    return dumps({"result": "SUCCESS","img_url": image_name})

def admin_user_result(token):
    if decode(token)['id'] != 1:
        return dumps({"result": "ERROR", "reason": "user with token is not an admin"})
    else:
        users = User.query.order_by(User.U_id).all()
        users_dicts = [user_to_dict(i) for i in users]
        return dumps({"customers": users_dicts})
    
    
