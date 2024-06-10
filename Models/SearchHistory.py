from main import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    search_history_id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.user_id'))
    actor_actress_id = db.Column(db.Integer, db.ForeignKey('actor_actress_table.actor_actress_id'))

    user = db.relationship('UserTable', backref=db.backref('search_histories', lazy=True))
    actor_actress = db.relationship('ActorActressTable', backref=db.backref('search_histories', lazy=True))
