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

app = Flask(__name__)
app.secret_key = 'squiggleballsI**())S*****D'

DBPREFIX = 'hax.antitree.com:%s'
A_RECORD_PREFIX = 'DNS:PASSTHRU:A:%s'
HOSTNAME = '.hax.antitree.com.'
WEBHOST = '.hax.antitree.com:8000'


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

def get_geo(ip):
    #gi = GeoIP.open("GeoLiteCity.dat", GeoIP.GEOIP_INDEX_CACHE | GeoIP.GEOIP_CHECK_CACHE)
    #print
    #print(ip)
    #print
    try:
        ipv4 = ipaddr.IPAddress(ip)
        if ipv4.is_private:
            return "Internal IP discovered"
    except:
        pass
    '''
    geo = gi.record_by_name(ip.strip())
    try:
        if not geo["city"]: geo["city"] = "Unknown"
        if not geo["region_name"]: geo["region_name"] = "Unknown"
        results = str(geo["city"]) + ', ' + str(geo["region_name"]) + ', ' + str(geo["country_name"])
    except Exception as err:
        print("Geo Error: %s" % err)
        results = "Unknown location"
    '''
    return ""

    return results

'''
Do I need this anymore?
@app.after_request
def add_cors(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
'''

@app.errorhandler(401)
def custom_401(error):
    return make_response('Invalid input', 401)

@app.route('/add', methods=['POST', 'GET'])
def add():
    print(request.json)
    if not request.json:
      return "Fail",401
    uid = request.json["uid"].lower()
    if not len(uid) == 36: abort(401)
    try:
        uuid.UUID(uid)
    except ValueError:
        abort(401)
    test = request.json["test"]
    if not test.isdigit(): abort(401)
    result = request.json["result"]
    testresult = result.split(',')
    for ip in testresult:
        try:
            _ipv4 = ipaddr.IPAddress(ip)
        except:
            abort(401)
    if True:  # Todo add validation
        dbrec = DBPREFIX % uid
        exists = r.hget(dbrec, test)  # find out if the rec exists
        if exists:
            print("Existing record found for %s" % uid)
            r.hset(dbrec, int(test), result)
        else:
            print("Adding new record for: %s" % uid)
            # Add the first url found

            #r.setex(A_RECORD_PREFIX % qname, peer[0], 30)
            #r.setex(DBPREFIX % uid + ':00', peer[0], 30)
            r.hset(dbrec, int(test), result)
        return "Success", 201
    else:
        return "Invalid test results", 500

@app.route('/v1/test', methods=['POST', 'GET'])
def api_redirect():
    uid = str(uuid.uuid4())  # The unique ID used as the key
    ip = request.remote_addr
    host = uid + '.hax.antitree.com.'
    chost = uid + WEBHOST
    url = 'http://04_' + chost + '/v1/results'
    r.hset(DBPREFIX % uid, '40', ip)
    session['uid'] = uid
    print(url)
    return redirect(url)


@app.route('/v1/results')
def api_results():
    try:
        uid = session["uid"]
        print("Found session cookie")
    except:
        print("Missing session cookie")
        uid = '0000'
    ips = validate(request.headers["Host"])
    return "%s" % ips

@app.route('/')
def slash():
    return redirect('/test')

@app.route('/reset')
def debug_reset():
    return "IPTables cancelled"
    table = iptc.Table(iptc.Table.FILTER)
    table.autocommit = False
    chain = iptc.Chain(table, "INPUT")
    for rule in chain.rules:
        chain.delete_rule(rule)
    table.commit()
    table.autocommit = True
            
    return "IPTables Flushed"

'''This is for dns rebinding attack, not tor
@app.route('/attack')
def attack():
    # make iptables rule to drop
    #chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    #rule = iptc.Rule()
    #rule.in_interface = "eth+"
    #rule.src = request.remote_addr
    #target = iptc.Target(rule, "DROP")
    #rule.target = target
    #chain.insert_rule(rule)
    host = request.headers["Host"]
    uid = host[:36]
    return render_template('attack.html',
        title="DNS Re-Bind Attack",
        subheader="I am attacking you",
        hostid=uid
    )

@app.route('/rebind')
def rebind():
    uid = str(uuid.uuid4())  # The unique ID used as the key
    ip = request.remote_addr
    host = uid + '.hax.antitree.com.'
    chost = uid + WEBHOST
    #r.set(A_RECORD_PREFIX % host, ip)
    return render_template('attack.html',
        title="DNS Re-Bind Attack",
        subheader="I am attacking you",
        hostid=str(random.randint(1,1024))
    )
'''

@app.route('/test')
def hello_world():
    uid = str(uuid.uuid4())  # The unique ID used as the key
    ip = request.remote_addr
    host = uid + '.hax.antitree.com.'
    chost = uid + WEBHOST
    r.hset(DBPREFIX % uid, '20', ip)
    #output = """<html><head><title>Tor Tester</title>
    #    <meta http-equiv="refresh" content="5;url=http://%s/results">
    #    <link rel="stylesheet" type="text/css" href="http://%s/mystyle.css">
    #    </head><body>""" % (chost, chost)
    #output += '<img style="visibility: hidden" src="http://%s/balls.jpg">' % chost
    #output += str(r.get(A_RECORD_PREFIX % host))
    return render_template('test.html',
        title="DNS Disbanding",
        subheader="Proof-of-concept DNS disbanding test tool",
        hostid=chost,
        uid=uid)


@app.route('/results', methods=['GET'])
def results():
    ips = validate(request.headers["Host"])  # make sure the host is correct
    tests = {}
    #tests["Flash"] = {
    #    "results": "",
    #    "desc": "Records the requesting DNS server from a flash plugin"
    #}
    #tests["JavaScript"] = {
    #    "results": "",
    #    "desc": "Test DNS leak via JavaScript calls"
    #}
    #tests["Redirect"] = {
    #    "results": "",
    #    "desc": "Test DNS leak via auto-redirect"
    #}
    tests["Web"] = {
        "results": "",
        "desc": "Your standard test to see the IP requesting the page"
    }
    tests["Web"]["results"] = [
            (request.remote_addr,
            get_geo(request.remote_addr))
        ]
    if "10" in ips:
        # lol
        tests["WebRTC"] = {
        "results": [("Test unsupported","")],
        "desc": "Test IP disclosure via WebRTC"
    }
        tests["WebRTC"]["results"] = [(ip,get_geo(ip)) for ip in set(ips["10"].split(','))]


    if "0" in ips:
        tests["DNS"] = {
        "results": "",
        "desc": "Test DNS leak via various remote resource inclusion"
    }
        tests["DNS"]["results"] = [(ip,get_geo(ip)) for ip in set(ips["0"].split(','))]

    print(ips)
    return render_template("results.html", tests=tests)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('about.html')


if __name__ == '__main__':
    r = redis.Redis(host="redis")
    app.run(host='0.0.0.0',debug=True)
