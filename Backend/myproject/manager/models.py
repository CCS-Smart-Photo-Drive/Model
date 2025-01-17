from myproject import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager

class Manager(db.Model):

    __tablename__ = 'managers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email , password):
        self.email = email 
        self.password_hash = generate_password_hash(password) #storing in hash for security

    def check_password(self, password):
        return check_password_hash(self.password_hash , password)

    def __repr__(self):
        return f"Manager email : {self.email}"
        

