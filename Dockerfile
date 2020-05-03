FROM python:3

ADD app.py /
ADD config.yml /
ADD requirements.txt /

COPY app.py app.py
COPY config.yml config.yml
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]