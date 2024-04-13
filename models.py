
from app import db
from sqlalchemy.orm import relationship

class TemporaryLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

class VerificationToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    token = db.Column(db.String(250), nullable=False)

class CabRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    destination = db.Column(db.String(250), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    creator_email = db.Column(db.String(250), nullable=False)

participants = db.Table('participants',
    db.Column('cab_request_id', db.Integer, db.ForeignKey('cab_request.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    
class JoinRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cab_request_id = db.Column(db.Integer, db.ForeignKey('cab_request.id'), nullable=False)
    requester_email = db.Column(db.String(250), nullable=False)
    accepted = db.Column(db.Boolean, default=False)  # Add this line
    cab_request = db.relationship('CabRequest', backref=db.backref('join_requests', lazy=True))
