import redis
import sys
import pickle
from utils import Singleton
from config import redis_configs, logging_configs
from models import MoviesModel
import logging


@Singleton
class MoviesCache:
    
    def __init__(self) -> None:
        self.prefix = "movies"
        self.max_ttl = 30

        logging.basicConfig(
            # filename=logging_configs['PATH'],
            # filemode='a',
            format='%(asctime)s  %(name)s  %(levelname)s  %(message)s',
            level=logging.INFO,
            handlers=[
                logging.FileHandler(logging_configs['PATH']),
                logging.StreamHandler()
            ]
        )

        self.client = self.redis_connect()

    
    def redis_connect(self):
        try:
            client = redis.Redis(
                host=redis_configs['HOST'],
                port=redis_configs['PORT'],
                password=redis_configs['PASSWORD'],
                db=0,
                socket_connect_timeout=5
            )
            ping = client.ping()
            if ping:
                logging.info(f"REDIS: Connected to the {redis_configs['HOST']}:{redis_configs['PORT']}")
                # print("REDIS: Conneted")
                return client
        
        except redis.AuthenticationError:
            logging.error(f"REDIS: AUTH ERROR for {redis_configs['HOST']}:{redis_configs['PORT']}")
            # print("REDIS: AUTH ERROR")
            sys.exit(1)
    
    def set_movie(self, movie_model):
        
        binary_movie_model = None
        key = ""

        if isinstance(movie_model, MoviesModel):
            binary_movie_model = pickle.dumps(movie_model.to_dict())
            key = self.prefix + '-' + str(movie_model.director) + '-' \
                + str(movie_model.name)
        
        elif isinstance(movie_model, dict):
            binary_movie_model = pickle.dumps(movie_model)
            key = self.prefix + '-' + str(movie_model['director']) + '-' \
                + str(movie_model['name'])
        
        else:
            logging.error(f"REDIS: key: {key} wrong instance for movie")
            raise("not an suitable instance")

        
        self.client.set(name=key, value=binary_movie_model)
        self.client.expire(name=key, time=self.max_ttl)

        logging.info(f"REDIS: key:{key} is cached")

        return True
    
    def get_movie(self, movie_name: str, movie_director: str):
        key = self.prefix + "-" + movie_name + "-" + movie_director
        
        binary_dict_movie = self.client.get(name=key)

        if binary_dict_movie:
            dict_movie = pickle.loads(binary_dict_movie)
            logging.info(f"REDIS: HIT key: {key} ")
            return dict_movie
        
        else:
            logging.info(f"REDIS: MISS key: {key}")
            return None
        
    def del_movie(self, movie_model):
        key = self.prefix + '-' + movie_model.director + "-" + movie_model.name;
        self.client.expire(name=key, time=0)
        logging.info(f"REDIS: delete key: {key} ")

    
    def set_all_movies(self, movies_list):
        
        _ls = []
        for movie in movies_list:
            _ls.append(movie.to_dict())
        
        key = self.prefix + '-' + 'all_movies'

        bin_ls = pickle.dumps(_ls)

        self.client.set(name=key, value=bin_ls)
        self.client.expire(name=key, time=self.max_ttl)

        logging.info(f"REDIS: key:{key} is cached")

        return True
    
    def get_all_movies(self):

        key = self.prefix + '-' + 'all_movies'

        bin_movies = self.client.get(name=key)

        if bin_movies:
            _ls = pickle.loads(bin_movies)
            logging.info(f"REDIS: HIT key: {key} ")
            return _ls
        
        else:
            logging.info(f"REDIS: MISS key: {key} ")
            return None
    
    def del_all_movies(self):
        key = self.prefix + '-' + 'all_movies'
        self.client.expire(name=key, time=0)    
        logging.info(f"REDIS: delete key: {key} ")
