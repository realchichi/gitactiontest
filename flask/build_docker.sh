#!/bin/sh


[ -e "$PWD"/.env.dev ] && . "$PWD"/.env.dev
app="BotaniBuzz"
docker build -t ${app} .
docker run -p 56700:8000 -d \
  --name=${app} \
  --network="mynetwork" \
  -e FLASK_DEBUG=${FLASK_DEBUG} \
  -v $PWD:/flask_app ${app}



