# Run a mysql server in docekr

## Start mysql server

```bash
export MYSQL_CONTAINER_NAME=mysql-dev
export ROOT_PASSWORD=1234
export MYSQL_IMAGE=mysql:8

docker run --name $MYSQL_CONTAINER_NAME -e MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD -d -p 3306:3306 $MYSQL_IMAGE

export MYSQL_SERVER_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql-dev)
```

## Manually grant privileges for remote accessing 

* Access container:

    ```bash
    docker exec -it $MYSQL_CONTAINER_NAME bash
    ```

* In container:  
  * `$ mysql -p`
  * grant privileges

    ```sql
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
    FLUSH PRIVILEGES;
    EXIT
    ```

    * Noted: create a new user for remote accesing is better.

* Test remote accessing
`docker run -it --network bridge --rm $MYSQL_IMAGE --host=$MYSQL_SERVER_HOST --user=root  --password=$ROOT_PASSWORD`

 --password=1234


docker run -p 3306:3306  --name mysql-dev -e MYSQL_ROOT_PASSWORD=1234 -d $MYSQL_IMAGE


# grant privileges for remote accessing
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;