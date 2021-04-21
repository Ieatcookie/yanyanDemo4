from server import *
from admin_function import *
from user_function import *

import json
from json import dumps


@app.route('/auth_login', methods=['POST'])
def customer_login():
    email = request.form["email"]
    password = request.form["password"]
    return dumps(auth_login(email, password))


@app.route('/customer_register', methods=['POST'])
def auth_register():
    email = request.form['email']
    password = request.form['password']
    nickname = request.form['nickname']
    repeat_password = request.form['repeat_password']
    mobile = request.form['mobile']
    return dumps(register(nickname, email, password, repeat_password, mobile))


@app.route('/customer_logout', methods=['POST'])
def customer_logout(token):
    token = request.form["token"]
    return dumps(auth_logout(token))

@app.route('/customer_search', methods=['POST'])
def customer_search():
    keyword = request.form["keyword"]
    token = request.form["token"]
    return dumps(find_pic_by_keywork(keyword, token))


@app.route('/cart_products', methods=['GET'])
def cart_products():
    IDs = request.args.get("productIds")
    return dumps(find_prods(IDs))


@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form["email"]
    password = request.form["password"]
    return dumps(adminLogin(email, password))


@app.route('/admin_products', methods=['GET'])
def admin_products():
    token = request.args.get("token")
    return dumps(admin_products_result(token))


@app.route('/get_user', methods=['POST'])
def get_user():
    token = request.form["token"]
    return dumps(find_user_by_token(token))


@app.route('/admin_orders', methods=['POST'])
def admin_orders():
    token = request.form["token"]
    return dumps(admin_orders_result(token))

@app.route('/admin_get_users', methods=['POST'])
def admin_get_users():
    token = request.form["token"]
    return dumps(admin_user_result(token))


@app.route('/manage_product', methods=['POST'])
def manage_product():
    token = request.form["token"]
    productId = request.form["productId"]
    newTitle = request.form["newTitle"]
    newDescription = request.form["newDescription"]
    newPrice = float(request.form["newPrice"])
    newQuantity = int(request.form["newQuantity"])
    newcategory = request.form["newcategory"]
    newDiscount = float(request.form["newDiscount"])
    images = request.form["images"]
    visible = request.form["is_visible"]
    return dumps(update_product(token, productId, newTitle, newDescription, newPrice, newQuantity, newcategory, newDiscount, images, visible))


@app.route('/manage_order', methods=['POST'])
def manage_order():
    token = request.form["token"]
    orderid = request.form["orderid"]
    status = request.form["status"]
    tracknumber = request.form["tracknumber"]
    a = change_order(token, orderid, status, tracknumber)
    print(a)
    return dumps(a)

@app.route('/all',methods = ['GET'])
def all():
    return dumps(get_all())

@app.route('/search_category', methods=['POST'])
def search_category():
    category = request.form["category"]
    return dumps(get_product_information_by_category(category))

@app.route('/upload_image', methods=['POST'])
def upload_image():
    token = request.form["token"]
    image = request.files["image"].read()
    Id = request.form["id"]
    return dumps(save_image_by_id(token, image, Id))

@app.route('/sort_all_products', methods=['POST'])
def sort_all_productss():
    id = request.form["id"]
    lower_bound = request.form["lower_bound"]
    higher_bound = request.form["higher_bound"]
    categories = request.form["categories"]
    x = sort_by_case(id, lower_bound, higher_bound, categories)
    print(x)
    return dumps(x)

@app.route('/get_product_by_id', methods=['POST'])
def get_product_by_id():
    id = request.form["id"]
    token = request.form["token"]
    return dumps(get_prod_by_id(id, token))

@app.route('/get_order_by_id', methods=['POST'])
def get_order_by_id():
    id = request.form["id"]
    return dumps(get_order(id))

@app.route('/processPayment', methods = ['POST'])
def processPayment():
    form = request.json
    token = form["token"]
    shipAddress = form["shipAddress"]["address"]
    billAddress = form["billAddress"]["address"]
    products = form["products"]
    comment = form["comment"]
    mobile = form["shipAddress"]["phone"]
    email = form["shipAddress"]["email"]
    sender_name = form["billAddress"]["name"]
    recieve_name = form["shipAddress"]["name"]
    return dumps(complete_order(token , recieve_name, products, shipAddress, billAddress, comment, mobile, email, sender_name))

@app.route('/chatBotQuery', methods = ['POST'])
def chatBotQuery():
    form = request.json
    token = form["token"]
    msg = form["query"]
    result = chatbot(token, msg)
    print(result)
    return dumps(result)

def get_analytic():
    return ''

@app.route('/collections',methods=['POST'])
def database():
    category = request.form["category"]
    return dumps(find_pic_by_category(category))

@app.route('/recommend', methods=['POST'])
def recommend():
    return dumps(admin_recommend())

@app.route('/guess_you_like', methods=['POST'])
def guess_you_like():
    token = request.form["token"]
    return guess(token)

@app.route('/send_code', methods=['POST'])
def reset_password():
    token = request.form["token"]
    x = auth_passwordreset_request(token)
    print(x)
    return dumps(x)

@app.route('/update_profile', methods = ['POST'])
def update_profile():
    email = request.form.get('email', type = str, default = None)
    password = request.form.get('password', type = str, default = None)
    nickname = request.form['name']
    token = request.form['token']
    mobile = request.form['mobile']
    reset_code = request.form.get('captcha', type = str, default = None)
    return dumps(edit_profile(email, password, nickname, token, mobile, reset_code))

@app.route('/order_history', methods = ['POST'])
def order_history():
    token = request.form['token']
    return dumps(users_orders(token))