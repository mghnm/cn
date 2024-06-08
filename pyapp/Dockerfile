FROM python:3.12-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    libpq-dev \
    python3-dev \
    build-essential

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD [ "uwsgi", "./app.ini" ]