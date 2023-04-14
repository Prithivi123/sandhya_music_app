FROM python:3.10.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /first_docker_app
COPY requirements.txt /first_docker_app/

RUN pip install -r requirements.txt
COPY . /first_docker_app/

CMD python3 manage.py runserver 0.0.0.0:8000