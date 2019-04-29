#!/bin/bash

docker rm -f passwords
docker run --name passwords -p 5432:5432 -e POSTGRES_DB=passwords -e POSTGRES_USER=passwords -e POSTGRES_PASSWORD=abc123!!! -d postgres
