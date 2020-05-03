FROM python:3

ADD app.py /
ADD config.yml /
ADD requirements.txt /

COPY app.py app.py
COPY config.yml config.yml
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

CMD [ "python", "app.py" ]