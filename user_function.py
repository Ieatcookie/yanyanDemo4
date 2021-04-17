import sys
from json import dumps
from datetime import datetime
import time
import uuid
import re
import hashlib
import random
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
def register(nickname, email, password, repeat_password, mobile):
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
    create_user(u_id, token, nickname, False, email, password, None, mobile)
    message = """\
    fivebluepetals\n\n\n 
    Hi dear """ + nickname + """.\nThanks for registering in fivebluepetals.com\n
    It's a confirmation that you registered successfully\n"""
    send_email(message, email)
    userr = u_id
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
    return dumps({"token": user.token, "userInfo": {
        "name": user.nickname,
        "id": user.U_id,
        "mobile":user.mobile,
        "password":user.password,
        "email":user.email
    }})


def auth_logout(token, user):
    user = user = User.query.filter_by(token=token)  # Finding user for given token
    if user is None:  # If there is no user corresponding to token
        return dumps({"result": "ERROR", "reason": "there is no user corresponding to token"})
    if user.state == 2:  # If user is already logged out
        return dumps({"result": "ERROR", "reason": "user is already logged out"})
    user.state = 2  # Changing the user's state to logged out
    return dumps({"result": "success"})


def find_pic_by_category(category):
    list_of_pro = []
    prods = Product.query.all()
    for p in prods:
        if p.if_shown == True and category in p.tags:
            list_of_pro.append(p)
    products = []

    for p in list_of_pro:
        products.append(product_to_dict(p))
    
    return dumps({"products": products})


def find_pic_by_keywork(keyword, token):
    user = User.query.filter_by(token = token).first()
    if user != None:
        create_Search_history(user.U_id, keyword)
    list_of_id = []
    prods = Product.query.all()
    for p in prods:
        if p.if_shown == True and keyword in p.name:
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
    reset_code = gen_reset_code()

    # Sending reset code to user by email
    # N: If this errors, this will be picked up by the error handler and an error will be shown
    msg = "Five Pedals RESET PASSWORD\n\n\nYou've requested to reset your password. Your reset code is : " + reset_code + "."
    send_email(em, msg)
    return dumps({"resetcode": reset_code})


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
        return dumps({"result": "ERROR", "reason": "there is no user corresponding to token"})
    if len(new_nickname) < 1 or len(new_nickname) > 50:
        return dumps({"result": "ERROR", "reason": "nickname must be between 1 and 50 characters."})
    user.nickname = new_nickname
    db.session.commit()
    dumps({"result": "success"})

def update_address(check_token, new_address):
    user = User.query.filter(User.token == check_token).first()  # Finding user for given token
    if user is None:  # If there is no user corresponding to token
        return dumps({"result": "ERROR", "reason": "there is no user corresponding to token"})
    user.address = new_address
    db.session.commit()
    dumps({"result": "success"})


def update_mobile(check_token, new_mobile):
    user = User.query.filter(User.token == check_token).first()  # Finding user for given token
    if user is None:  # If there is no user corresponding to token
        return dumps({"result": "ERROR", "reason": "there is no user corresponding to token"})
    if new_mobile.isdecimal() == False:  # If there is no user corresponding to token
        return dumps({"result": "ERROR", "reason": "there is no user corresponding to token"})
    user.mobile = new_mobile
    db.session.commit()
    dumps({"result": "success"})


def update_email(check_token, new_email):
    user = User.query.filter(User.token == check_token).first()  # Finding user for given token
    if user is None:  # If there is no user corresponding to token
        return dumps({"result": "ERROR", "reason": "there is no user corresponding to token"})
    result = valid_email(new_email)
    if result == -1:
        return dumps({"result": "ERROR", "reason": "email already registered"})
    elif result == 0:
        return dumps({"result": "ERROR", "reason": "Invalid email"})
    user.email = new_email
    db.session.commit()
    dumps({"result": "success"})


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
    return_list1 = []
    for pro in products:
        if categories in pro.tags:
            return_list1.append(pro)
    product_dicts = []
    for i in return_list1:
        product_dicts.append(product_to_dict(i))
    return dumps({"products": product_dicts})


def include_category(product, categories):
    int_to_cate = {
        '1': "Love flowers",
        '2': "Friendship flowers",
        '3': "Birthday flowers",
        '4': "Greeting flowers",
        '5': "Repay the teacher",
        '6': "Visiting and condolences",
        '7': "Apology flowers",
        '8': "Wedding flowers"
    }
    cs = categories.split(",")
    pcs = product.tags.split(",")
    for pc in pcs:
        for c in cs:
            if int_to_cate[c] == pc:
                return True
    return False

'''
1 : A-Z
2 : Z-A
3 : price high to low
4 : price low to high
5 : stock low to high
6 : stock high to low
'''
def sort_by_case(case, low, high, categories):
    case = int(case)
    low = int(low)
    high = int(high)
    products = []
    prods = []
    if high < low:
        return dumps({"result": "ERROR", "reason": "the upper bond should be lower than lower bound."})
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
        if i.if_shown == True and high >= i.price and low <= i.price and include_category(i, categories) is True:
            prods.append(product_to_dict(i))
    return dumps({"products": prods})

def get_all():
    return_list1 = []
    prods = Product.query.all()
    for p in prods:
        return_list1.append(p)
    product_dicts=[product_to_dict(i) for i in return_list1]
    return dumps({"products":product_dicts}) 


def get_prod_by_id(ID, token):
    id = int(ID)
    print("#####", token)
    user = User.query.filter_by(token = token).first()
    if user != None:
        c_h = Click_history.query.filter_by(U_id = user.U_id, P_id = id).first()
        if c_h == None:
            create_Click_history(user.U_id, id)
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

def admin_recommend():
    return get_product_information_by_category("recommend")

def add_to_cart(productINFO):
    id_quant = productINFO.split('?')
    id = int(id_quant[0])
    quant = int(id_quant[1])
    product = Product.query.filter_by(pro_id = id).first()
    if product.stock < quant:
        return dumps({"result": "ERROR", "reason": "not enough stock"})
    return dumps({"result": "success"})


def if_user_viewed(U_id, P_id):
    c_h = Click_history.query.filter_by(U_id = U_id, P_id = P_id).first()
    if c_h == None:
        return False
    return True

def num_search_to_favor(U_id, p_name, p_tag):
    count_keyword = 0
    count_category = 0
    historys = Search_history.query.filter_by(U_id = U_id).all()
    for history in historys:
        if history.search in p_name:
            count_keyword = count_keyword + 1
        if history.search in p_tag:
            count_category = count_category + 1
    
    return count_category * 3 + count_keyword * 6

def random_product_id(length, n):
    i = 0
    l_of_id = []
    while i != 4:
        x = round(random.uniform(1, length) * random.uniform(1, length)) % length + 1
        if x not in l_of_id:
            l_of_id.append(x)
            i = i + 1

    return l_of_id

#if customer viewed this item before, there is higher possibility that the product get recomm
#if customer searched related term before, there will also be higher possibility that the product get recomm
#but not high as click history
#product with more stock will get recomm with hgiher askdhfkala posibillity
def guess(token):
    user = User.query.filter_by(token = token).first()
    products = Product.query.order_by(Product.stock.desc()).all()
    length = len(products)
    product_list = []
    if user == None:
        list_of_id = random_product_id(length, 20)
        while len(list_of_id) > 0:
            number = list_of_id.pop(0)
            for p in products: 
                if  p.pro_id == number:
                    product_list.append(p)
    else:
        p_favor = {}
        i = length
        u_id = user.U_id
        for p in products:
            fav_num = i * 10 /length
            if if_user_viewed(u_id, p.pro_id) == True:
                fav_num = fav_num + 30
            fav_num = fav_num + num_search_to_favor(user.U_id, p.name, p.tags)
            p_favor[p] = fav_num
            i = i - 1
        product_list = sorted(p_favor, key=p_favor.get, reverse=True)
    dict_list = []
    for p in product_list:
        dict_list.append(product_to_dict(p))
    return dict_list
        
        
        
        

