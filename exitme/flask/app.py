from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import abort
from flask import make_response
import random
import uuid
import redis
#import GeoIP
#import iptc # iptables for re-bind attack
import ipaddr

SECRET_ANSWER = 'BOURGET_SHENANIGANS'

app = Flask(__name__)
WINIPS = ['94.242.55.221','94.242.55.220', '94.242.57.198']

def validate(host):
    # check qname format
    try:
        uid = host[3:39]
        uuid.UUID(uid)
    except ValueError:
        print("UID failed")
        return False

    if not len(host.split('.')[0]) == 39:
        print("Len fail")
        return False

    if not host[-(len(WEBHOST)):] == WEBHOST:
        print("CORS fail")
        return False

    newhost = uid + HOSTNAME

    #ips = r.get(A_RECORD_PREFIX % newhost)
    ips = r.hgetall(DBPREFIX % uid)
    if ips:
        return ips
    else:
        print("No ips for %s" % newhost)
        return False


@app.errorhandler(401)
def custom_401(error):
    return make_response('Invalid input', 401)

@app.route('/')
def slash():
    ip = request.remote_addr
    return redirect('/ip/%s' % ip)

@app.route('/ip/<postid>')
def ip(postid):
    if str(postid) in WINIPS:
        return "You Win! %s" % SECRET_ANSWER
    else:     
        return make_response("Whatever %s" % postid, 401)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
