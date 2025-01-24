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

class Events(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    organised_by = db.Column(db.String(120), nullable=False)

    image_embeddings = db.relationship('ImageEmbedding', backref='event', lazy=True)

    def __init__(self, event_name, date, description, organised_by):
        self.event_name = event_name
        self.date = date
        self.description = description
        self.organised_by = organised_by

    def __repr__(self):
        return f"Event name: {self.event_name}, Date: {self.date}, Organised by: {self.organised_by}"

class ImageEmbedding(db.Model):

    __tablename__ = 'image_embeddings'

    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.String(120), nullable=False)
    embedding = db.Column(db.PickleType, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    event_name = db.Column(db.String(120), nullable=False)
    def __init__(self, event_id, image_name, embedding , event_name):
        self.event_id = event_id
        self.image_name = image_name
        self.embedding = embedding
        self.event_name = event_name
    def __repr__(self):
        return f"ImageEmbedding(event_id={self.event_id}, image_name={self.image_name})"




