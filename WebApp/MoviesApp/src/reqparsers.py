from flask_restful import reqparse
from models import MoviesModel

# movie_arg_parser

movie_arg_parser = reqparse.RequestParser()

movie_arg_parser.add_argument('name', type=str, help="", required=False)
movie_arg_parser.add_argument('director', type=str, help="", required=False)
movie_arg_parser.add_argument('year', type=int, \
    help="year is a requiered integer number",
    required=True)
movie_arg_parser.add_argument('imdb', type=float, \
    help="imdb is a float number")
movie_arg_parser.add_argument('rotten_tomatoes', type=int, \
    help="rotten_tomatoes is an integer number")


class MoviesFormParser:
    
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help="", required=True)
    parser.add_argument('director', type=str, help="", required=True)
    parser.add_argument('year', type=int, \
        help="year is a requiered integer number",
        required=True)
    
    parser.add_argument('imdb', type=float, \
        help="imdb is a float number", required=False)
    parser.add_argument('rotten_tomatoes', type=int, \
        help="rotten_tomatoes is an integer number", required=False)

    @staticmethod
    def parse_args():
        args = MoviesFormParser.parser.parse_args()

        filtered_args = {}
        for key, value in args.items():
            if value is not None:
                filtered_args[key] = value
        
        return filtered_args
        

