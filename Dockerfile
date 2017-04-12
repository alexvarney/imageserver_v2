FROM python:3.4-alpine
ADD ./src /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN pip install gunicorn
EXPOSE 8081
CMD gunicorn --bind 0.0.0.0:8081 imageserver:app
