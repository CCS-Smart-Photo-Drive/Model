import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_KEY")  

db = SQLAlchemy(app)
Migrate(app,db)

@app.route('/')
def index():
    return "This is home page"

jwt = JWTManager(app)


from myproject.member.views import member_bp
app.register_blueprint(member_bp, url_prefix='/member')

from myproject.manager.views import manager_bp
app.register_blueprint(manager_bp , url_prefix='/manager')

