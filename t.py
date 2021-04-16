from db import *
us = User.query.all()
for u in us:
    print(u.token)