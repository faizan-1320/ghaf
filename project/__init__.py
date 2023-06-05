from flask import Flask,jsonify,g
import os
from flask_jwt_extended import JWTManager
from datetime import timedelta
import mysql.connector # pip install mysql-connector
from .advertisment import advertisement_bp

app=Flask(__name__)

app.secret_key='user'

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

app.register_blueprint(advertisement_bp)