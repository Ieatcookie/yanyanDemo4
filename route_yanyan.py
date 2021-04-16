from server import *
#&Code for Haowei
#home page
@app.route('/',methods=['GET'])
def home():
    return render_template("/Yanyan/home.html")
    
#return login page
@app.route('/login',methods=['GET'])
def login():
    return render_template("/Yanyan/login.html")

@app.route('/register',methods=['GET'])
def register():
    return render_template("/Yanyan/register.html")

@app.route('/sort_all_product',methods=['POST'])
def sort_all_product():
    return sort_by_stock()

@app.route('/shop',methods=['GET'])
def shop():
    return render_template("/Yanyan/product.html")

@app.route('/product_detail',methods=['GET'])
def singleproduct():
    return render_template("/Yanyan/productDetail.html")

@app.route('/category',methods=['GET'])
def category():
    return render_template("/Yanyan/category.html")

@app.route('/collection',methods=['GET'])
def collection():
    return render_template("/Yanyan/collection.html")

@app.route('/mine',methods=['GET'])
def mine():
    return render_template("/Yanyan/mine.html")

@app.route('/cart',methods=['GET'])
def cart():
    return render_template("/Yanyan/cart.html")

