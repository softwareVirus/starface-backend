from main import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

gender_enum = ENUM('Male', 'Female', 'Other', name='gender_enum', create_type=False)

class ActorActressTable(db.Model):
    __tablename__ = 'actor_actress_table'
    actor_actress_id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    biography = db.Column(db.String(1000))
    img_url = db.Column(db.String(300))

def __repr__(self):
        return f"<ActorActressTable(firstName={self.firstName}, lastName={self.lastName}, age={self.age}, gender={self.gender})>"