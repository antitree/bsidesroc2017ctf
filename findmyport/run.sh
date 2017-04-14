#!/bin/bash
DIR="$(dirname "${BASH_SOURCE[0]}")"
docker kill bsidesroc-find-my-port
docker rm bsidesroc-find-my-port
docker run -d --name bsidesroc-find-my-port -p 9822:80 -v ${PWD}/www:/usr/share/nginx/html:ro nginx
