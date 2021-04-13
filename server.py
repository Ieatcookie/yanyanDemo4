from flask import Flask, render_template, request
from user_function import *
from db import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BFP.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.app_context().push()
#db.drop_all()
db.create_all()
#load_data()

from route_yanyan import *
from route_haowei import *
from route_backend import *

if __name__ == '__main__':
    app.run(debug=True)