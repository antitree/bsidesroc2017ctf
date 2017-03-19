#!/bin/bash
DIR="$(dirname "${BASH_SOURCE[0]}")"
cd $DIR
docker-compose kill
docker-compose rm -f
docker-compose up -d
