FROM python:3.9-slim-buster

WORKDIR /src
COPY /Greppo-canal-stat-

RUN pip3 install -r requirements.txt

CMD ["greppo", "serve", "app.py", "--host=127.0.0.1:8080"]
