FROM python:3.8

WORKDIR /code
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 8000
COPY . .
