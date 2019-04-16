#!/bin/bash
BASEDIR=$(dirname "$0")

export MYSQL_CONTAINER_NAME=mysql-dev
export USER=root
export ROOT_PASSWORD=1234
export MYSQL_IMAGE=mysql:8
export GRANT_PRIVILEGES_SCRIPT=tmp.sql

cat << EOF > $GRANT_PRIVILEGES_SCRIPT
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
EOF

docker run --name $MYSQL_CONTAINER_NAME -e MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD -d -p 3306:3306 $MYSQL_IMAGE

# wait service to be ready
sleep 30s

# copy $GRANT_PRIVILEGES_SCRIPT then execute it.
docker cp $GRANT_PRIVILEGES_SCRIPT $MYSQL_CONTAINER_NAME:/$GRANT_PRIVILEGES_SCRIPT
docker exec $MYSQL_CONTAINER_NAME sh -c "mysql --user=$USER  --password=$ROOT_PASSWORD < /$GRANT_PRIVILEGES_SCRIPT"

export MYSQL_SERVER_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql-dev)

pipenv run python $BASEDIR/init_db.py

rm $GRANT_PRIVILEGES_SCRIPT