from flask import Flask
from flask_restful import Api

from views import *
from config import flask_configs


app = Flask(__name__)

api = Api(app)

api.add_resource(Movies, "/api/movies/")
api.add_resource(MovieByName, "/api/movie/<string:name>")
api.add_resource(ExactMovie, "/api/director/<string:dir_name>/movie/<string:name>/")
api.add_resource(MovieEdit, "/api/edit/movie/")
api.add_resource(DirectorsMovies, "/api/director/<string:director_name>/")
api.add_resource(MoviesSearch, "/api/search/")

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(
        debug=flask_configs['debug'],
        port=flask_configs['port'],
        host=flask_configs['host']
    )