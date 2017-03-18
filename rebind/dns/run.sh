#!/bin/bash
docker kill rebind-dns-test
docker rm -f rebind-dns-test
docker run -td -p 53535:53/udp --name rebind-dns-test rebind-dns
