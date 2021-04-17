from server import *
from admin_function import *
from user_function import *
import json


@app.route('/auth_login', methods=['POST'])
def customer_login():
    email = request.form["email"]
    password = request.form["password"]
    return auth_login(email, password)


@app.route('/customer_register', methods=['POST'])
def auth_register():
    email = request.form['email']
    password = request.form['password']
    nickname = request.form['nickname']
    repeat_password = request.form['repeat_password']
    mobile = request.form['mobile']
    return register(nickname, email, password, repeat_password, mobile)


@app.route('/customer_logout', methods=['POST'])
def customer_logout(token):
    token = request.form["token"]
    return auth_logout(token)


@app.route('/customer_search', methods=['POST'])
def customer_search():
    keyword = request.form["keyword"]
    token = request.form["token"]
    return find_pic_by_keywork(keyword, token)


@app.route('/cart_products', methods=['GET'])
def cart_products():
    IDs = request.args.get("productIds")
    return find_prods(IDs)


@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.form["email"]
    password = request.form["password"]
    return adminLogin(email, password)


@app.route('/admin_products', methods=['GET'])
def admin_products():
    token = request.args.get("token")
    return admin_products_result(token)


@app.route('/get_user', methods=['POST'])
def get_user():
    token = request.form["token"]
    return find_user_by_token(token)


@app.route('/admin_orders', methods=['POST'])
def admin_orders():
    token = request.form["token"]
    return admin_orders_result(token)

@app.route('/admin_get_users', methods=['POST'])
def admin_get_users():
    token = request.form["token"]
    return admin_user_result(token)


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
    return update_product(token, productId, newTitle, newDescription, newPrice, newQuantity, newcategory, newDiscount, images)


@app.route('/manage_order', methods=['POST'])
def manage_order():
    token = request.form["token"]
    orderid = request.form["orderid"]
    status = request.form["status"]
    tracknumber = request.form["tracknumber"]
    return update_order(token, orderid, status, tracknumber)


@app.route('/edit_nickname', methods=['POST'])
def edit_nickname():
    token = request.form["token"]
    new_nickname = request.form["nickname"]
    return update_nickname(token, new_nickname)


@app.route('/edit_address', methods=['POST'])
def edit_address():
    token = request.form["token"]
    new_address = request.form["address"]
    return update_address(token, new_address)

@app.route('/all',methods = ['GET'])
def all():
    return get_all()

@app.route('/edit_email', methods=['POST'])
def edit_email():
    token = request.form["token"]
    new_email = request.form["email"]
    return update_email(token, new_email)


@app.route('/edit_mobile', methods=['POST'])
def edit_mobile():
    token = request.form["token"]
    new_mobile = request.form["mobile"]
    return update_mobile(token, new_mobile)


@app.route('/search_category', methods=['POST'])
def search_category():
    # this token needs to be added in the future
    # token = request.form["token"]
    category = request.form["category"]
    return get_product_information_by_category(category)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    # this token needs to be added in the future
    # token = request.form["token"]
    token = request.form["token"]
    image = request.files["image"].read()
    Id = request.form["id"]
    return save_image_by_id(token, image, Id)

@app.route('/sort_all_products', methods=['POST'])
def sort_all_productss():
    id = request.form["id"]
    lower_bound = request.form["lower_bound"]
    higher_bound = request.form["higher_bound"]
    return sort_by_case(id, lower_bound, higher_bound)

@app.route('/get_product_by_id', methods=['POST'])
def get_product_by_id():
    id = request.form["id"]
    token = request.form["token"]
    return get_prod_by_id(id, token)

@app.route('/collections',methods=['POST'])
def database():
    category = request.form["category"]
    return find_pic_by_category(category)

@app.route('/recommend', methods=['POST'])
def recommend():
    return admin_recommend()

@app.route('/guess_you_like', methods=['POST'])
def guess_you_like():
    token = request.form["token"]
    return guess(token)

