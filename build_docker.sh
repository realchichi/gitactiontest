#!/bin/sh
<<<<<<< HEAD
=======

>>>>>>> 2b7ddc8ecab70a11aaba85d952354282224b5d7f
[ -e "$PWD"/.env.dev ] && . "$PWD"/.env.dev
app="docker.project"
docker build -t ${app} .
docker run -p 56700:8000 -d \
  --name=${app} \
<<<<<<< HEAD
  --network="mynetwork" \
  -e FLASK_DEBUG=${FLASK_DEBUG} \
  -v $PWD:/flask_app ${app}



=======
  -e FLASK_DEBUG=${FLASK_DEBUG} \
  -v $PWD:/flask_app ${app}
>>>>>>> 2b7ddc8ecab70a11aaba85d952354282224b5d7f
