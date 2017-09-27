#!/usr/bin/env bash

# Using the official mariadb docker container.
# https://store.docker.com/images/mariadb

docker pull mariadb
docker run --name syco-mariadb -v `pwd`/syco-mariadb/default.d:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mariadb:latest
docker run --name syco-mariadb -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mariadb:latest


# Connect to the mariadb
# docker run -it --link syco-mariadb:mysql --rm mariadb sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD"'

# Bash access
# docker exec -it syco-mariadb bash



