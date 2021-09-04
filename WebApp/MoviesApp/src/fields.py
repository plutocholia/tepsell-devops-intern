
from flask_restful import fields

movies_fields = {
    'director': fields.String,
    'year': fields.Integer,
    'name': fields.String,
    'imdb': fields.Float,
    'rotten_tomatoes': fields.Integer
}

