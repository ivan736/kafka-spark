# Run a mysql server in docker

## Start mysql server

### Option 1: with script

* execute [create_env.sh](create_env.sh)
    * `./create_env.sh`

### Option 2:

* This section describes the required steps to set up a mysql

* exports environment variables

    ```bash
    export MYSQL_CONTAINER_NAME=mysql-dev
    export ROOT_PASSWORD=1234
    export MYSQL_IMAGE=mysql:8

    docker run --name $MYSQL_CONTAINER_NAME -e MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD -d -p 3306:3306 $MYSQL_IMAGE

    export MYSQL_SERVER_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql-dev)
    ```

* manually grant privileges for remote accessing
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
`docker run -it --rm $MYSQL_IMAGE --host=$MYSQL_SERVER_HOST --user=root  --password=$ROOT_PASSWORD`


# grant privileges for remote accessing
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;