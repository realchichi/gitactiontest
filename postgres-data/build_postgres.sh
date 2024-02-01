#!/bin/sh

name="test"
docker build -t ${name} .
docker run -p 5432:5432 -d\
 --name=${name}\
 --network="mynetwork"\
 -e POSTGRES_PASSWORD="password"\
 -e POSTGRES_USER="postgres"\
 -e POSTGRES_DB="db" \
 -v pgdatavolume:"/var/lib/postgresql/data"\
 postgres

 # docker exec -it ${name} createdb -U postgres -h localhost -p 5432 db

