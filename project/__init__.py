from flask import Flask,jsonify,g
import os
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from datetime import timedelta
import mysql.connector
from .admin import admin_bp
from .authentication import authentication_bp
from .fishmarket import fishmarket_bp
from .product import product_bp
from .store import store_bp
from .supermarket import supermarket_bp
from .user import user_bp
from .advertisement import advertisement_bp
from .order import order_bp

app=Flask(__name__)

@app.before_request
def before_request():
    try:
        g.db=mysql.connector.connect(
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD'],
            host=os.environ['MYSQL_HOST'],
            database=os.environ['MYSQL_DB']
        )
    except:
        return jsonify({"Message":"Start Server"})

@app.after_request
def after_request(response):
    try:
        g.db.close()
        return response
    except:
        return jsonify({"Message":"Start Server"})


app.config['JWT_SECRET_KEY']=os.environ['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(days=1)
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']

jwt = JWTManager(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'faizandiwan921@gmail.com'
app.config['MAIL_PASSWORD'] = 'dsxrvtuspfrhsjah'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.register_blueprint(admin_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(fishmarket_bp)
app.register_blueprint(product_bp)
app.register_blueprint(store_bp)
app.register_blueprint(supermarket_bp)
app.register_blueprint(user_bp)
app.register_blueprint(advertisement_bp)
app.register_blueprint(order_bp)