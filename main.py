import os
from flask import Flask, jsonify, request, abort
from flask import request
from sqlalchemy.inspection import inspect
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from datetime import datetime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import text, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, current_user
from datetime import timedelta
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash

# Assuming MovieTable is in a folder named 'models' and file named 'movie_table.py'

# Configure database credentials
username = quote_plus("buraktm")
password = quote_plus("Patatesseverim35.")
hostname = "starface-postgres.postgres.database.azure.com"
port = 5432
database = "starface_db"
DATABASE_URL = f"postgresql://{username}:{password}@{hostname}:{port}/{database}?sslmode=require"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db = SQLAlchemy(app)

class JWTConfig:
    # Secret key to sign JWT tokens (you should keep this secret and not hardcode it here)
    SECRET_KEY = 'your_secret_key'
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    # Token expiration time
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


app.config.from_object(JWTConfig)

jwt = JWTManager(app=app)


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class UserRole(enum.Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'

class ActorActressTable(db.Model):
    __tablename__ = 'actor_actress_table'
    actor_actress_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    biography = db.Column(db.String(1000))
    img_url = db.Column(db.String(300))

    def to_dict(self):
        return {
            'actor_actress_id': self.actor_actress_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'age': self.age,
            'gender': self.gender,
            'biography': self.biography,
            'img_url': self.img_url
        }


class MovieActorActressManyToManyTable(db.Model):
    __tablename__ = 'movie_actor_actress_many_to_many_table'
    many_to_many_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie_table.movie_id'))
    actor_actress_id = db.Column(db.Integer, db.ForeignKey('actor_actress_table.actor_actress_id'))
    series_id = db.Column(db.Integer, db.ForeignKey('series_table.series_id'))

    movie = db.relationship('MovieTable', backref=db.backref('movie_actors_actresses', lazy=True))
    actor_actress = db.relationship('ActorActressTable', backref=db.backref('movie_actors_actresses', lazy=True))
    series = db.relationship('SeriesTable', backref=db.backref('series_actors_actresses', lazy=True))

class MovieTable(db.Model):
    __tablename__ = 'movie_table'
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(100))
    movie_detail = db.Column(db.String(500))
    imdb_rating = db.Column(db.Float(2))
    release_date = db.Column(db.DateTime)
    img_url = db.Column(db.String(300))

    def to_dict(self):
        def safe_date(date):
            try:
                return date.replace(year=1970).isoformat() if date else None
            except ValueError:
                return None

        return {
            'movie_id': self.movie_id,
            'movie_name': self.movie_name,
            'movie_detail': self.movie_detail,
            'imdb_rating': float(self.imdb_rating) if self.imdb_rating else None,
            'release_date': safe_date(self.release_date),
            'img_url': self.img_url
        }

class SeriesTable(db.Model):
    __tablename__ = 'series_table'
    series_id = db.Column(db.Integer, primary_key=True)
    series_name = db.Column(db.String(100))
    series_detail = db.Column(db.String(500))
    imdb_rating = db.Column(db.Float(2))
    starting_date = db.Column(db.DateTime)
    finish_date = db.Column(db.DateTime)
    season_number = db.Column(db.Integer)
    img_url = db.Column(db.String(300))

    def to_dict(self):
        def safe_date(date):
            try:
                return date.replace(year=1970).isoformat() if date else None
            except ValueError:
                return None

        return {
            'series_id': self.series_id,
            'series_name': self.series_name,
            'series_detail': self.series_detail,
            'imdb_rating': float(self.imdb_rating) if self.imdb_rating else None,
            'starting_date': safe_date(self.starting_date),
            'finish_date': safe_date(self.finish_date),
            'season_number': self.season_number,
            'img_url': self.img_url
        }
class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    search_history_id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.user_id'))
    actor_actress_id = db.Column(db.Integer, db.ForeignKey('actor_actress_table.actor_actress_id'))

    user = db.relationship('UserTable', backref=db.backref('search_histories', lazy=True))
    actor_actress = db.relationship('ActorActressTable', backref=db.backref('search_histories', lazy=True))

    def __init__(self, user_id, actor_actress_id):
        self.user_id = user_id
        self.actor_actress_id = actor_actress_id
        self.created_date = datetime.utcnow()

    

class UserTable(db.Model):
    __tablename__ = 'user_table'
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50)) 
    email = db.Column(db.String(100), unique=True)
    hashed_password = db.Column(db.String(512))
    avatar = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    roles = db.Column(ENUM(UserRole), nullable=False, default="USER")

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'avatar': self.avatar,
            'gender': self.gender,
            'created_date': self.created_date.isoformat() if self.created_date else None,
            'updated_date': self.updated_date.isoformat() if self.updated_date else None,
            'is_verified': self.is_verified,
            'roles': self.roles.value  # Enum değerini string olarak döndürmek için
        }

class VerificationCodeTable(db.Model):
    __tablename__ = 'verification_code_table'
    verification_code_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    email = db.Column(db.String(50))
    is_valid = db.Column(db.Boolean)


@jwt.user_identity_loader
def user_identity_loader(user):
    """
    Callback function to get the identity of the current user.
    Parameters
    ----------
    user : User
        The current user.
    Returns
    -------
    str
        The user's identity (user ID).
    """
    print(user)
    return str(user.to_dict()["user_id"])

@jwt.user_lookup_loader
def user_lookup_loader(_jwt_header, jwt_data):
    """
    Callback function to look up a user by identity in JWT data.
    Parameters
    ----------
    _jwt_header : dict
        The JWT header (not used in this function).
    jwt_data : dict
        The JWT data containing the user's identity.
    Returns
    -------
    User
        The user associated with the provided identity.
    """
    identity = jwt_data["sub"]
    return UserTable.query.filter_by(user_id=identity).first()

@app.route('/')
def test_database_connection():
    try:
        # Simple query using SQLAlchemy to test the database connection
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 'Hello, PostgreSQL!' AS Message"))
            message = result.fetchone()[0]
            return jsonify(message=message)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/films/<int:movie_id>', methods=['GET'])
def get_film(movie_id):
    print("Route is loaded")
    movie = MovieTable.query.filter_by(movie_id=movie_id).first()
    if movie:
        return jsonify(movie.to_dict())
    else:
        return jsonify({"error": "Movie not found"}), 404

# TODO: yeni oluşturulacak hesabın var olup olmadığı kontrol edilecek.
# TODO: Response olarak Access Token dönmesi gerekiyor ve
# oluşturulan hesabın response bilgileri arasından password ve rol çıkarılmalı.
@app.route('/signup', methods=["POST"])
def sign_up_post():
    data = request.get_json()
    if not data:
        abort(400, description="No data provided")

    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')
    avatar = data.get('avatar')
    gender = data.get('gender')

    if not all([firstname, lastname, email, password]):
        abort(400, description="Missing required fields")

    hashed_password = password#generate_password_hash(password)

    new_user = UserTable(
        firstname=firstname,
        lastname=lastname,
        email=email,
        hashed_password=hashed_password,
        avatar=avatar,
        gender=gender
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        # Create an access token
        access_token = create_access_token(identity=new_user, expires_delta=timedelta(hours=24))

        user_data = new_user.to_dict()
        user_data['token'] = access_token

        return jsonify({"message": "User created successfully", "user": user_data, "token": access_token}), 201
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    if not data:
        abort(400, description="No data provided")

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        abort(400, description="Missing required fields")

    user = UserTable.query.filter_by(email=email).first()

    if user and user.hashed_password == password:#check_password_hash(user.hashed_password, password):
        # Create an access token
        access_token = create_access_token(identity=user, expires_delta=timedelta(hours=24))

        user_data = user.to_dict()
        user_data['token'] = access_token

        return jsonify({"message": "Login successful", "user": user_data, "token": access_token}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    return jsonify({"message": "Login successful", "user": current_user.to_dict()}), 200

from sqlalchemy.orm import joinedload
"""
.options(
        joinedload(ActorActressTable.movie_actors_actresses).joinedload(MovieActorActressManyToManyTable.movie),
        joinedload(ActorActressTable.movie_actors_actresses).joinedload(MovieActorActressManyToManyTable.series)
    ).
        movie_actor.movie.to_dict() 
            for movie_actor in actor_actress.movie_actors_actresses if movie_actor.movie
            movie_actor.series.to_dict() 
            for movie_actor in actor_actress.movie_actors_actresses if movie_actor.series
        
    """
@app.route('/actor/<int:actor_actress_id>', methods=['GET'])
def get_actor(actor_actress_id):
    print("Get actor information.")
    actor_actress = ActorActressTable.query.filter_by(actor_actress_id=actor_actress_id).first()
    
    if actor_actress:
        # Extract related movies and series
        related_movies = []
        related_series = [
        ]

        return jsonify({
            "actor": actor_actress.to_dict(),
            "movies": related_movies,
            "series": related_series
        })
    else:
        print(actor_actress_id, actor_actress)
        return jsonify({"Error": "Actor/Actress not found."}), 404

# TODO: Bitmemiş bir diziyi çektiğimizde year -1 hatası veriyor.
@app.route('/series/<int:series_id>', methods=['GET'])
def get_series(series_id):
    print("Get actor information.")
    series = SeriesTable.query.filter_by(series_id=series_id).first()
    if series:
        return jsonify(series.to_dict())
    else:
        return jsonify({"Error": "Series not found."}), 404


def tuple_to_dict(t):
    return {
        'id': t[0],
        'first_name': t[1],
        'last_name': t[2],
        'age': t[3],
        'gender': t[4],
        'bio': t[5],
        'imdb_link': t[6],
    }

@app.route('/history/<int:page>/<int:limit>', methods=['GET'])
@jwt_required()
def get_history(page, limit):
    try:
        page = page - 1
        cr_user = current_user
        if not cr_user:
            return 'User not found', 404

        result = db.engine.connect().execute(text(f'''
            SELECT * FROM public.actor_actress_table 
            WHERE actor_actress_table.actor_actress_id IN 
                (SELECT actor_actress_id FROM search_history WHERE user_id = {cr_user.user_id})
            LIMIT {limit} OFFSET {page * limit}
        '''))
        rows = result.fetchall()
        json_ready_data = [tuple_to_dict(entry) for entry in rows]
        print(json_ready_data, cr_user, cr_user.user_id)
        return jsonify({
            "actors": json_ready_data
        })
    except Exception as e:
        return str(e), 500


@app.route('/history', methods=['POST'])
@jwt_required()
def post_history():
    try:
        data = request.get_json()
        actor_id = data.get('actor_id')

        cr_user = current_user
        if not cr_user:
            return 'User with ID {} not found'.format(current_user.user_id), 404

        actor = SearchHistory.query.filter_by(actor_actress_id=actor_id, user_id=current_user.user_id).first()
        if actor is None:
            new_history = SearchHistory(user_id=current_user.user_id, actor_actress_id=actor_id)
            db.session.add(new_history)
            db.session.commit()
        return 'History updated successfully', 200
    except Exception as e:
        print(e)
        return str(e), 500
    
@jwt_required()
@app.route('/search/<string:search_type>/<string:search_string>', methods=['GET'])
def get_search(search_type, search_string):
    try:
        if search_type == "actor":
            actors = ActorActressTable.query.filter(ActorActressTable.firstname.ilike(search_string + '%')).all()
            actors_list = [{'actor_actress_id': actor.actor_actress_id, 'firstname': actor.firstname, 'lastname': actor.lastname, 'age': actor.age, 'gender': actor.gender, 'biography': actor.biography, 'img_url': actor.img_url} for actor in actors]
            print(actors_list)
            return jsonify({
                'actors': actors_list
            })
        elif search_type == "movie":
            movies = MovieTable.query.filter(MovieTable.movie_name.ilike(search_string + '%')).all()
            movie_list = [{
                'movie_id': movie.movie_id,
                'movie_name': movie.movie_name,
                'movie_detail': movie.movie_detail,
                'imdb_rating': movie.imdb_rating,
                'release_date': movie.release_date.strftime('%Y-%m-%d') if movie.release_date else 'Not Available',
                'img_url': movie.img_url
            } for movie in movies]
            return jsonify({
                "movies":movie_list
            })
        elif search_type == "series":
            series = SeriesTable.query.filter(SeriesTable.series_name.ilike(search_string + '%')).all()
            series_list = [{
                'series_id': serie.series_id,
                'series_name': serie.series_name,
                'series_detail': serie.series_detail,
                'imdb_rating': serie.imdb_rating,
                'starting_date': serie.starting_date.strftime('%Y-%m-%d') if serie.starting_date else 'Not Available',
                'finish_date': serie.finish_date.strftime('%Y-%m-%d') if serie.finish_date else 'Not Available',
                'season_number': serie.season_number,
                'img_url': serie.img_url
            } for serie in series]
            return jsonify({
                "series": series_list
            })
    except Exception as e:
        print(e)
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@app.route('/delete_actor/<int:actor_id>', methods=['DELETE'])
def delete_actor():
    actor_actress = ActorActressTable.query.get(actor_actress_id)
    if actor_actress is None:
        return jsonify({'error': 'Actor or actress not found'}), 404

    db.session.delete(actor_actress)
    db.session.commit()
    return jsonify({'message': 'Actor or actress deleted successfully'}), 200

@app.route('/delete_series/<int:series_id>', methods=['DELETE'])
def delete_series(series_id):
    series = SeriesTable.query.get(series_id)
    if series is None:
        return jsonify({'error': 'Series not found'}), 404

    db.session.delete(series)
    db.session.commit()
    return jsonify({'message': 'Series deleted successfully'}), 200

@app.route('/delete+movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = MovieTable.query.get(movie_id)
    if movie is None:
        return jsonify({'error': 'Movie not found'}), 404

    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted successfully'}), 200


@app.route('/add_actor_actress', methods=['POST'])
def add_actor_actress():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    firstname = data.get('firstname')
    lastname = data.get('lastname')
    age = data.get('age')
    gender = data.get('gender')
    biography = data.get('biography')
    img_url = data.get('img_url')

    if not all([firstname, lastname, age, gender, biography, img_url]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_actor_actress = ActorActressTable(
        firstname=firstname,
        lastname=lastname,
        age=age,
        gender=gender,
        biography=biography,
        img_url=img_url
    )

    db.session.add(new_actor_actress)
    db.session.commit()

    return jsonify(new_actor_actress.to_dict()), 201


@app.route('/add_series', methods=['POST'])
def add_series():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Zorunlu alanların kontrolü
    if not all([key in data for key in ['series_name', 'series_detail', 'imdb_rating', 'starting_date', 'finish_date', 'season_number','img_']]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Veri çekme ve tür dönüşümleri
    try:
        series_name = data['series_name']
        series_detail = data['series_detail']
        imdb_rating = float(data['imdb_rating'])
        starting_date = datetime.strptime(data['starting_date'], '%Y-%m-%d')
        finish_date = datetime.strptime(data['finish_date'], '%Y-%m-%d')
        season_number = int(data['season_number'])
        img_url = data['img_url']
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    # Yeni dizi nesnesinin oluşturulması
    new_series = SeriesTable(
        series_name=series_name,
        series_detail=series_detail,
        imdb_rating=imdb_rating,
        starting_date=starting_date,
        finish_date=finish_date,
        season_number=season_number,
        img_url=img_url
    )

    db.session.add(new_series)
    db.session.commit()

    return jsonify(new_series_id=new_series.series_id), 201


@app.route('/add_movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Zorunlu alanların kontrolü
    if not all(key in data for key in ['movie_name', 'movie_detail', 'imdb_rating', 'release_date', 'img_url']):
        return jsonify({'error': 'Missing required fields'}), 400

    # Veri çekme ve tür dönüşümleri
    try:
        movie_name = data['movie_name']
        movie_detail = data['movie_detail']
        imdb_rating = float(data['imdb_rating'])
        release_date = datetime.strptime(data['release_date'], '%Y-%m-%d')
        img_url = data['img_url']
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    # Yeni film nesnesinin oluşturulması
    new_movie = MovieTable(
        movie_name=movie_name,
        movie_detail=movie_detail,
        imdb_rating=imdb_rating,
        release_date=release_date,
        img_url=img_url
    )

    db.session.add(new_movie)
    db.session.commit()

    return jsonify(new_movie_id=new_movie.movie_id), 201


if __name__ == '__main__':
    app.run(host="192.168.229.133", port=5000, debug=True)
