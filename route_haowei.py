from server import *
#&Code for Haowei
@app.route('/admin',methods=['GET'])
def admin():
    return render_template("/Haowei/admin/admin_login.html")

@app.route('/admin_portal',methods=['GET'])
def admin_portal():
    return render_template("/Haowei/admin/admin_portal.html")

@app.route('/cart',methods=['GET'])
def cart():
    return render_template("/Haowei/cart.html")

@app.route('/productList',methods=['GET'])
def productList():
    token = request.args.get("token")
    products=[]
    products = json.loads(admin_products_result(token))['products']
    return render_template("/Haowei/admin/product_list.html",products=products)

@app.route("/manageProduct",methods=['GET'])
def manageProduct():
    token = request.args.get("token")
    id = request.args.get("id")
    product = {}
    if(id is not None):
        product = product_to_dict(getProductById(id))
    print(product,"ssssssssssssssssssssssssss")
    return render_template("/Haowei/admin/manage_product.html",product=product)

@app.route('/customerList',methods=['GET'])
def customerList():
    token = request.args.get("token")
    customers = json.loads(admin_user_result(token))['customers']
    #print(customers)
    test_data = {
        "id":0,
        "name": "haowei lou",
        "email": "louhaowei@gmail.com",
        "phone": "0406111111",
        "address":"Haymarkey, Sydney, 2000, NSW",
        "orders":["0"]
    }
    customers.append(test_data)
    return render_template("/Haowei/admin/customer_list.html",customers=customers)

@app.route('/manageCustomer',methods=['GET'])
def manageCustomer():
    token = request.args.get("token")
    id = request.args.get("id")
    test_data = {
        "id":0,
        "name": "haowei lou",
        "email": "louhaowei@gmail.com",
        "phone": "0406111111",
        "address":"Haymarkey, Sydney, 2000, NSW",
        "orders":["0"]
    }
    customer = test_data
    return render_template("/Haowei/admin/manage_customer.html",customer=customer)

@app.route('/orderList',methods=['GET'])
def orderList():
    token = request.args.get("token")
    products=[]
    orders = json.loads(admin_orders_result(token))['orders']
    test_customer = {
        "id":0,
        "name": "haowei lou",
        "email": "louhaowei@gmail.com",
        "phone": "0406111111",
        "address":"Haymarkey, Sydney, 2000, NSW",
        "orders":["0"]
    }
    test_data = {
        "id":0,
        "time":"2021/03/01 17:35:41",
        "customer":test_customer,
        "products" : json.loads(find_prods("0;1"))['products'],
        "quantity" : [1,2],
        "status":"paid",
        "shippingAddress":test_customer['address'],
        "billingAddress":test_customer['address'],
        "tracking":None
    }
    print(test_data['products'])
    orders.append(test_data)
    return render_template("/Haowei/admin/order_list.html",orders=orders)

@app.route('/manageOrder',methods=['GET'])
def manageOrder():
    token = request.args.get("token")
    id = request.args.get("id")
    order = {}
    test_customer = {
        "id":0,
        "name": "haowei lou",
        "email": "louhaowei@gmail.com",
        "phone": "0406111111",
        "address":"Haymarkey, Sydney, 2000, NSW",
        "orders":["0"]
    }
    test_data = {
        "id":0,
        "time":"2021/03/01 17:35:41",
        "customer":test_customer,
        "products" : json.loads(find_prods("0;1"))['products'],
        "quantity" : [1,2],
        "status":"paid",
        "shippingAddress":test_customer['address'],
        "billingAddress":test_customer['address'],
        "tracking":None
    }
    order = test_data
    return render_template("/Haowei/admin/manage_order.html",order=order)

