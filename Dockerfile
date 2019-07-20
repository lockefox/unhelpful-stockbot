FROM revolutionsystems/python:3.7.1

COPY . /opt/unhelpful-bot

# TODO USER

WORKDIR /opt/unhelpful-bot
RUN pip3 install .

RUN pip3 freeze
