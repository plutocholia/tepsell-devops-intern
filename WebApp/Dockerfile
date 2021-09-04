FROM ubuntu:latest

RUN apt-get update -y && apt-get install -y python3-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./MoviesApp/ /app/MoviesApp/

WORKDIR /app/MoviesApp/src

# CMD [ "python3", "-m" , "flask", "run", "--host=127.0.0.1", "--port=8080"]

# CMD [ "python3", "-m" , "gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

CMD python3 -m gunicorn --bind 0.0.0.0:8080 app:app
