FROM heywill/will-base:3.7-alpine

RUN apk upgrade --update
RUN apk add openssl-dev libffi-dev

COPY . /opt/will

# TODO USER

WORKDIR /opt/will
RUN pip3 install -r requirements.txt

RUN pip3 freeze
