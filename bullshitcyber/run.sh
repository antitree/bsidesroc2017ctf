#!/bin/bash
DIR="$(dirname "${BASH_SOURCE[0]}")"
docker kill bsidesroc-bullshitcyber
docker rm bsidesroc-bullshitcyber
docker run -d --name bsidesroc-bullshitcyber -p 7788:80 -v ${PWD}/www:/usr/share/nginx/html:ro nginx
