import sys
from json import dumps
from datetime import datetime
import time
import uuid
import re
import hashlib
# from flask_cors import CORS
from flask import Flask, request, jsonify
from db import *
import jwt
import smtplib
from email import encoders 
from email.header import Header 
from email.mime.text import MIMEText 
from email.utils import parseaddr 
from email.utils import formataddr 

# from flask_mail import Mail, Message
users = []
online = []


def print_email():
    users = User.query.all()
    for u in users:
        print(u.email)


#####################################################################################
#                                                                                   #
#                               AUTHENTICATION FUNCTIONS                            #
#                                                                                   #
#####################################################################################
# REGISTRATION FUNCTION
# @app.route("/auth/register", methods=["POST"])
def register(nickname, email, password, repeat_password):
    '''user = User.query.filter_by(email = "994114654@qq.com").first()
    db.session.delete(user)
    db.session.commit()'''
    # Getting the email from server
    # CHECKS FOR INVALID INFORMATION BELOW
    # Checking whether email is valid
    result = valid_email(email)
    print_email()
    if result == -1:
        return dumps({"result": "ERROR", "reason": "email already registered"})
    elif result == 0:
        return dumps({"result": "ERROR", "reason": "Invalid email"})
    if len(password) < 5 or len(password) > 50:
        return dumps({"result": "ERROR", "reason": "password's length must be between 5- 50 characters."})
    if len(nickname) < 1 or len(nickname) > 50:
        return dumps({"result": "ERROR", "reason": "nickname must be between 1 and 50 characters."})
    if password != repeat_password:
        return dumps({"result": "ERROR", "reason": "password not match with repeat password"})

    password = hashpass(password)  # Hashing the password for storage

    users = User.query.all()
    u_id = 10000 + len(users)
    token = get_token(int(u_id))  # Getting token
    # Creating a user and setting variables of the user
    create_user(u_id, token, nickname, False, email, password, None, None)
    message = """\
    fivebluepetals\n\n\n 
    Hi dear """ + nickname + """.\nThanks for registering in fivebluepetals.com\n
    It's a confirmation that you registered successfully\n"""
    #send_email(message, email)
    return dumps({"customer": {'nickname': nickname, 'email': email, 'token': token}})


def auth_login(em, input_password):
    # CHECKS FOR INVALID INFORMATION BELOW
    result = valid_email(em)
    print(result)
    if result == 1:
        return dumps({"result": "ERROR", "reason": "Email is not registered."})
    elif result == 0:
        return dumps({"result": "ERROR", "reason": "Invalid Email."})
    # Finding u_id associated with token
    user = User.query.filter_by(email=em).first()

    # Checking matching passwords
    input_password = hashpass(input_password)
    if input_password != user.password:
        return dumps({"result": "ERROR", "reason": "Password is incorrect."})

    user.is_online = True  # Setting state to logged in
    db.session.commit()

    return dumps({"token": user.token, "userInfo": {"name": user.nickname, "id": user.U_id}})


def auth_logout(token, user):
    user = user = User.query.filter_by(token=token)  # Finding user for given token
    if user is None:  # If there is no user corresponding to token
        return dumps({"is_success": False, "reason": "there is no user corresponding to token"})
    if user.state == 2:  # If user is already logged out
        return dumps({"is_success": False, "reason": "user is already logged out"})
    user.state = 2  # Changing the user's state to logged out
    return dumps({"is_success": True})


def find_pic_by_category(category):
    list_of_pro = []
    prods = Product.query.all()
    for p in prods:
        if category in p.tags:
            list_of_pro.append(p)
    products = []

    for p in list_of_pro:
        products.append(product_to_dict(p))

    return dumps({"products": products})


def find_pic_by_keywork(keyword):
    list_of_id = []
    prods = Product.query.all()
    for p in prods:
        if keyword in p.name:
            list_of_id.append(p)
    product_dicts = []
    for p in list_of_id:
        product_dicts.append(product_to_dict(p))
    return dumps({"products": product_dicts})


# @app.route('/', methods=["GET"])  # this actually cannot work now
def auth_passwordreset_request(em):
    # email = str(request.args.get("email"))
    result = valid_email(em)
    print(result)
    if result == 1:
        return dumps({"result": "ERROR", "reason": "Email is not registered."})
    elif result == 0:
        return dumps({"result": "ERROR", "reason": "Invalid Email."})
    # Finding u_id associated with token
    user = User.query.filter_by(email=em).first()
    reset_code = gen_reset_code()  # Generating reset code

    # Sending reset code to user by email
    # N: If this errors, this will be picked up by the error handler and an error will be shown
    msg = "Five Pedals RESET PASSWORD\n\n\nYou've requested to reset your password. Your reset code is : " + reset_code + "."
    send_email(em, msg)
    return {}


def auth_passwordreset_reset(reset_code, new_password):
    if reset_code is None:
        raise ValueError(f"Invalid reset code.")
    user = get_user_for_reset_code(reset_code)
    if user is None:
        raise ValueError(f"Invalid reset code.")
    # Check whether the password given is valid
    if len(new_password) > 5:
        user.password = hashpass(new_password)
    else:
        raise ValueError(f"Invalid password.")
    user.reset_code = None  # Resetting reset code to None
    return {"is_success": True}


# register and login helper function
def get_user_for_reset_code(reset_code):
    for user in users:
        if user.reset_code == reset_code:
            return user
    return None


def valid_email(em):
    low_em = em.lower()
    if re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', low_em):
        user = User.query.filter_by(email=em).first()
        print(user, em)
        if user == None:
            return 1  # email not in use
        else:
            return -1  # returns -1 for existing email
    else:
        return 0  # returns 0 for invalid email


def hashpass(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_token(u_id):
    curr_time = datetime.now()
    token = jwt.encode({"u_id": u_id, "time": curr_time.isoformat()}, 'fivebluepetals', algorithm='HS256')
    return token


def gen_reset_code():
    reset_code = uuid.uuid4().hex
    return reset_code


def send_email(receiver_email, message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("liyun8185@126.com", "123456")
        server.sendmail("liyun8185@126.com", receiver_email, message)


def update_nickname(check_token, new_nickname):
    user = User.query.filter(User.token == check_token).first()  # Finding user for given token
    if user is None:  # If there is no user corresponding to token
        return dumps({"is_success": False, "reason": "there is no user corresponding to token"})
    """""
    if user.is_online == 2:  # If user is already logged out
        return dumps({"is_success": False, "reason": "user is already logged out"})
    """""
    user.nickname = new_nickname
    db.session.commit()


def update_address(check_token, new_address):
    user = User.query.filter(User.token == check_token).first()  # Finding user for given token
    if user is None:  # If there is no user corresponding to token
        return dumps({"is_success": False, "reason": "there is no user corresponding to token"})
    """""
    if user.is_online == 2:  # If user is already logged out
        return dumps({"is_success": False, "reason": "user is already logged out"})
    """""
    user.address = new_address
    db.session.commit()


def update_email(check_token, new_email):
    user = User.query.filter(User.token == check_token).first()  # Finding user for given token
    if user is None:  # If there is no user corresponding to token
        return dumps({"is_success": False, "reason": "there is no user corresponding to token"})
    """""
    if user.is_online == 2:  # If user is already logged out
        return dumps({"is_success": False, "reason": "user is already logged out"})
    """""
    user.email = new_email
    db.session.commit()


def update_mobile(check_token, new_mobile):
    user = User.query.filter(User.token == check_token).first()  # Finding user for given token
    if user is None:  # If there is no user corresponding to token
        return dumps({"is_success": False, "reason": "there is no user corresponding to token"})
    """""
    if user.is_online == 2:  # If user is already logged out
        return dumps({"is_success": False, "reason": "user is already logged out"})
    """""
    user.mobile = new_mobile
    db.session.commit()


# this method needs to add token in the future
def get_product_information_by_category(categories):
    products = Product.query.all()
    print(products)
    return_list1 = []
    for pro in products:
        if categories in pro.tags:
            return_list1.append(pro)
    product_dicts = []
    for i in return_list1:
        product_dicts.append(product_to_dict(i))
    return dumps({"products": product_dicts})

'''
1 : A-Z
2 : Z-A
3 : price high to low
4 : price low to high
5 : stock low to high
6 : stock high to low
'''
def sort_by_case(case):
    case = int(case)
    products = []
    prods = []
    if case == 1:
        products = Product.query.order_by(Product.name, Product.stock).all()
    if case == 2:  
        products = Product.query.order_by(Product.name.desc(), Product.stock).all()
    if case == 3:  
        products = Product.query.order_by(Product.price.desc(), Product.stock).all()
    if case == 4:  
        products = Product.query.order_by(Product.price, Product.stock).all()
    if case == 5:  
        products = Product.query.order_by(Product.stock, Product.price.desc()).all()
    if case == 6:  
        products = Product.query.order_by(Product.stock.desc(), Product.price.desc()).all()
    if case > 6 or case < 0:
        return dumps({"result": "ERROR", "reason": "Number is not valid."})
    for i in products:
        prods.append(product_to_dict(i))
    return dumps({"products": prods})

def get_all():
    return_list1 = []
    prods = Product.query.all()
    for p in prods:
        return_list1.append(p)
    product_dicts=[product_to_dict(i) for i in return_list1]
    return dumps({"products":product_dicts}) 


def get_prod_by_id(ID):
    id = int(ID)
    return dumps({"products": [product_to_dict(Product.query.filter_by(pro_id = id).all()[0])]})

def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))

def send_email(content, reciever_email):
    from_email = "liyun8185@126.com"
    from_email_pwd = "123456"
    smtp_server = "smtp.126.com"  
    msg = MIMEText("<html><body><h3>hello</h3><p>" + content + "</p></body></html>", "html", "utf-8")
    msg["From"] = format_addr("%s" %(from_email))
    msg["To"] = format_addr("%s" %(reciever_email))
    msg["Subject"] = Header("python email", "utf-8").encode()
    
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_email, from_email_pwd)
    server.sendmail(from_email, [reciever_email], msg.as_string())
    server.quit()