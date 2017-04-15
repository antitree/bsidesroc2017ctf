#!/bin/bash
DIR="$(dirname "${BASH_SOURCE[0]}")"
docker kill bsidesroc-nas4mat
docker rm bsidesroc-nas4mat
docker run -d --name bsidesroc-nas4mat -p 7000:80 -v ${PWD}/src/public:/usr/share/nginx/html:ro nginx
