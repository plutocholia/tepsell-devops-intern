CREATE DATABASE IF NOT EXISTS db_movies;

USE db_movies;

DROP TABLE IF EXISTS Movies;

CREATE TABLE Movies (
    director varchar(50) NOT NULL,
    year INT NOT NULL,
    name varchar(60) NOT NULL,
    imdb FLOAT DEFAULT NULL,
    rotten_tomatoes INTEGER DEFAULT NULL,
    PRIMARY KEY (director, name)
);


INSERT INTO Movies (director, year, name, imdb, rotten_tomatoes) VALUES 
    ("Craig Gillespie", 2021, "Cruella", 7.4, 73),
    ("Hirokazu Koreeda", 2004, "Nobody Knows", 8.1, 83),
    ("David Lynch", 1977, "Eraserhead", 7.4, 91),
    ("David Lynch", 1997, "Lost Highway", 7.6, 60),
    ("David Lynch", 2001, "Mulholland Dr.", 7.9, 83),
    ("Jean-Luc Godard", 1960, "Breathless", 7.8, 81),
    ("Jean-Luc Godard", 1963, "Contempt", 7.6, 94)
;