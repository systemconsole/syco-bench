#!/usr/bin/env bash
docker run -it --rm --name syco-bench -v `pwd`:/usr/src/syco-bench --link syco-mariadb:mysql syco-bench bash
