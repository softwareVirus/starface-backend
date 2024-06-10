from flask_restful import Resource, fields, marshal_with, abort
from Models.ActorActressTable import ActorActressTable

actor_actress_serialized = {
    'actor_actress_id': fields.Integer,
    'firstName': fields.String,
    'lastName': fields.String,
    'age': fields.Integer,
    'gender': fields.String,
    'biography': fields.String,
    'img_url': fields.String,
}

class ActorActress(Resource):
    @marshal_with(actor_actress_serialized)
    def get(self, actor_actress_id):
        result = ActorActressTable.query.filter_by(actor_actress_id=actor_actress_id).first()
        if not result:
            abort(404, message="Could not find the Actor/Actress.")
        return result
