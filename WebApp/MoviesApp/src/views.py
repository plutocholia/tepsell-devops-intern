from flask_restful import Resource, abort, marshal_with
from sqlalchemy.exc import IntegrityError

from config import *
from models import session, MoviesModel
from reqparsers import movie_arg_parser, MoviesFormParser
from fields import movies_fields
from caching import MoviesCache

class MovieByName(Resource):
    @marshal_with(movies_fields)
    def get(self, name):
        movies = session.query(MoviesModel).filter_by(name=name).all()
        if not movies:
            abort(404, message=f"there is no movie called {name}")
        return movies, 200

class Movies(Resource):
    @marshal_with(movies_fields)
    def get(self):
        cache = MoviesCache.Instance()
        
        movies = cache.get_all_movies()
        
        if not movies:
            movies = session.query(MoviesModel).all()
            cache.set_all_movies(movies)

        return movies, 200
    
    @marshal_with(movies_fields)
    def post(self):

        filtered_args = MoviesFormParser.parse_args()
        
        try:
            movie = MoviesModel(**filtered_args)

            session.add(movie)
            session.commit()

            cache = MoviesCache.Instance()
            cache.set_movie(movie)
            cache.del_all_movies()

        except IntegrityError as e:
            session.rollback()
            abort(400, message=\
                f"{filtered_args['name']} from {filtered_args['director']} is duplicate")

        return movie, 200

class MoviesSearch(Resource):
    def __init__(self):
        Resource.__init__(self)
        
    @marshal_with(movies_fields)
    def get(self):
        filtered_args = MoviesFormParser.parse_args()
        
        cache = MoviesCache.Instance()
        
        
        movie = cache.get_movie(filtered_args['director'], filtered_args['name'])

        if movie:
            return movie, 200

        movies = session.query(MoviesModel).filter_by(**filtered_args).all()
        
        if not movies:
            abort(404, message="no matches")
        return movies, 200


class MovieEdit(Resource):
    @marshal_with(movies_fields)
    def post(self):
        args = movie_arg_parser.parse_args()
        
        filtered_args = {}
        for key, value in args.items():
            if value is not None:
                filtered_args[key] = value
        
        res_movie = session.query(MoviesModel).filter_by(\
            director=filtered_args['director'],
            name=filtered_args['name']).first()
        
        if res_movie:

            if 'imdb' in args:
                res_movie.imdb = args['imdb']
            if 'rotten_tomatoes' in args:
                res_movie.rotten_tomatoes = args['rotten_tomatoes']
            if 'year' in args:
                res_movie.year = args['year']
        
            session.commit()

            cache = MoviesCache.Instance()
            cache.set_movie(res_movie)

        else:
            abort(404, message=f"there is no such movie to edit")

        return res_movie, 200

class DirectorsMovies(Resource):
    @marshal_with(movies_fields)
    def get(self, director_name):
        movies = session.query(MoviesModel).filter_by(\
            director=director_name).all()
        
        if not movies:
            abort(404, message=f"there id no director called {director_name}")
        
        return movies, 200

class ExactMovie(Resource):

    @marshal_with(movies_fields)
    def get(self, dir_name: str, name: str):

        cache = MoviesCache.Instance()
        cached_movie = cache.get_movie(dir_name, name)
        
        if cached_movie:
            cache.set_movie(cached_movie)
            return cached_movie, 200
        
        else:

            movie = session.query(MoviesModel).filter_by(name=name, \
                director=dir_name).first()

            if not movie:
                abort(404, \
                    message=f"there is no movie with name of {name} \
                        and director of {dir_name}")
            
            cache.set_movie(movie)

            return movie, 200