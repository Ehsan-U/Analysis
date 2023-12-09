FROM python:3.10.6-slim-buster
WORKDIR /app
COPY . /app

RUN apt update -y

RUN apt-get update -y && pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]
