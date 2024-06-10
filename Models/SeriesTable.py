from main import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

class SeriesTable(db.Model):
    __tablename__ = 'series_table'
    series_id = db.Column(db.Integer, primary_key=True)
    series_name = db.Column(db.String(100))
    series_detail = db.Column(db.String(500))
    imdb_rating = db.Column(db.Float(2))
    starting_date = db.Column(db.DateTime)
    finish_date = db.Column(db.DateTime)
    season_number = db.Column(db.Integer)