from myproject import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager

class Member(db.Model):

    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, email , password):
        self.email = email 
        self.password_hash = generate_password_hash(password) #storing in hash for security

    def check_password(self, password):
        return check_password_hash(self.password_hash , password)

    def __repr__(self):
        return f"User email : {self.email}"
        

