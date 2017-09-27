#!/usr/bin/env bash
docker run -it --rm --name syco-bench -v `pwd`:/usr/src/syco-bench syco-bench bash

#docker exec -it syco-mariadb bash
