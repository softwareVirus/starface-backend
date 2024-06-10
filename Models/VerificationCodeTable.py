from main import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

class VerificationCodeTable(db.Model):
    __tablename__ = 'verification_code_table'
    verification_code_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    email = db.Column(db.String(50))
    is_valid = db.Column(db.Boolean)
