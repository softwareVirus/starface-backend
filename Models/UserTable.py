from main import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

class UserRole(db.Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'

class UserTable(db.Model):
    __tablename__ = 'user_table'
    user_id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    email = db.Column(db.String(50))
    hashed_password = db.Column(db.String(128))
    avatar = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_verified = db.Column(db.Boolean)
    roles = db.Column(ENUM(UserRole), nullable=False)