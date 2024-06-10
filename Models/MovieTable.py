from main import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

class MovieTable(db.Model):
    __tablename__ = 'movie_table'
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(100))
    movie_detail = db.Column(db.String(500))
    imdb_rating = db.Column(db.Float(2))
    release_date = db.Column(db.DateTime)
    img_url = db.Column(db.String(300))

    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'movie_name': self.movie_name,
            'movie_detail': self.movie_detail,
            'imdb_rating': float(self.imdb_rating) if self.imdb_rating else None,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'img_url': self.img_url
        }