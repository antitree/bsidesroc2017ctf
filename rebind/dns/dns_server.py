#!/usr/bin/python
# Author: AntiTree
# Custom DNS resolver service
# based on:
#   https://github.com/gleicon/python_dns_servers/blob/master/gevent_dns.py


import gevent
from gevent import socket
#import gevent.dns;
from gevent import monkey
monkey.patch_socket()

import redis
import uuid
from dnslib import *

# added sys to use stdout
from sys import stdout

HOSTNAME = 'hax.antitree.com.'  # requires ending "."
WEBSERVER = 'treebind.antitree.com'
DBPREFIX = 'hax.antitree.com:%s'

A_RECORD_PREFIX = 'DNS:PASSTHRU:A:%s'
TXT_RECORD_PREFIX = 'DNS:PASSTHRU:TXT:%s'
CNAME_RECORD_PREFIX = 'DNS:PASSTHRU:CNAME:%s'

AF_INET = 2
SOCK_DGRAM = 2

s = socket.socket(AF_INET, SOCK_DGRAM)
s.bind(('', 53))
#s.bind(('', 53535))  ##  debug

def validate(request):

    # Check request type is always A
    try:
        if not request.q.qtype == QTYPE.A:
            print("Wrong fucking query type")
            return False
    except:
        pass

    # check Make sure it starts with a UID
    qname = str(request.q.qname)
    try:
        uuid.UUID(qname[3:39])
    except ValueError:
        print("Invalid UID %s" % qname[3:39])
        return False

    if not qname.lower()[-(len(HOSTNAME)):] == HOSTNAME:
        return False

    # check length just in case
    if not len(qname) == (len(str(uuid.uuid4())) + 4 + len(HOSTNAME)):
        print("Invalid length")
        return False

    return True

def dns_handler(s, peer, data, r, ip):
    '''
    Dns server that only response to A records
    with a specific IP. The function takes in:
    socket, peer IP address, DNS data record,
    redis instance, and legitimate IP address to respond with
    '''

    request = DNSRecord.parse(data)
    id = request.header.id
    qname = request.q.qname

    # Validate request
    if validate(request):
        qname = request.q.qname  # Host name requested
        uid = str(qname)[3:39].lower()  # extract UID from request
        test = 0
        dbrec = DBPREFIX % uid
        exists = r.hget(dbrec, test)  # find out if the rec exists
        if exists:
            print("Existing record found for %s" % uid)
            if not exists == peer[0]:
                print("Appending UID")
                # Append url to redis keys
                r.hset(dbrec, test, peer[0])
                ##  TODO SET expiry
        else:
            print("Adding new record for: %s" % uid)
            # Add the first url found

            #r.setex(A_RECORD_PREFIX % qname, peer[0], 30)
            #r.setex(DBPREFIX % uid + ':00', peer[0], 30)
            r.hset(dbrec, test, peer[0])

        print("Request (%s): %r (%s) - Response: %s" % (
            str(peer),
            qname.label,
            QTYPE[QTYPE.A],
            ip
        ))
    else:
        print("Request dropped from %s for %s" % (peer[0], qname))
        ip = '127.0.0.1'

    reply = DNSRecord(DNSHeader(id=id, qr=1, aa=1, ra=1), q=request.q)
    #reply.add_answer(RR(qname, QTYPE.A, ttl=60, rdata=A('172.16.100.55')))
    reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip)))
    s.sendto(reply.pack(), peer)


def run(ip='0.0.0.2'):
    # DEBUG
    ip = socket.gethostbyname(WEBSERVER)

    r = redis.Redis(host='redis')
    while True:
        data, peer = s.recvfrom(8192)
        gevent.spawn(dns_handler, s, peer, data, r, ip)

if __name__ == '__main__':
    run()
