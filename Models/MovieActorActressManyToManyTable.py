from main import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

class MovieActorActressManyToManyTable(db.Model):
    __tablename__ = 'movie_actor_actress_many_to_many_table'
    many_to_many_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie_table.movie_id'))
    actor_actress_id = db.Column(db.Integer, db.ForeignKey('actor_actress_table.actor_actress_id'))
    series_id = db.Column(db.Integer, db.ForeignKey('series_table.series_id'))

    movie = db.relationship('MovieTable', backref=db.backref('movie_actors_actresses', lazy=True))
    actor_actress = db.relationship('ActorActressTable', backref=db.backref('movie_actors_actresses', lazy=True))
    series = db.relationship('SeriesTable', backref=db.backref('series_actors_actresses', lazy=True))