
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:itsUbuntu@localhost/db_movies2', echo=True)

# Creating table
Base = declarative_base()

class MoviesModel(Base):
    __tablename__ = 'movies_model'
    name = Column(String(50), nullable=False, primary_key=True)
    director = Column(String(50), nullable=False, primary_key=True)
    year = Column(Integer, nullable=False)
    score = Column(Float, nullable=True)

Base.metadata.create_all(engine)


# Adding data
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

session.add_all([
    MoviesModel(director="Craig Gillespie",     year=2021, name="Cruella",          score=7.4),
    MoviesModel(director="Hirokazu Koreeda",    year=2004, name="Nobody Knows",     score=8.1),
    MoviesModel(director="David Lynch",         year=1977, name="Eraserhead",       score=7.4),
    MoviesModel(director="David Lynch",         year=1997, name="Highway",          score=7.6),
    MoviesModel(director="David Lynch",         year=2001, name="Mulholland Dr.",   score=7.9),
    MoviesModel(director="Jean-Luc Godard",     year=1960, name="Breathless",       score=7.8),
    MoviesModel(director="Jean-Luc Godard",     year=1963, name="Contempt",         score=7.6)
])

session.commit()