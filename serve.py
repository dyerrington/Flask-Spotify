#!./bin/python

from subprocess import call
from flask import Flask, session, redirect, url_for, escape, request
import time, os
 
app = Flask(__name__)

def save_timestamp():
    timestamp = time.time()
    fp = open('timestamp', 'w')
    fp.write(str(int(timestamp)))
    print 'saving', str(int(timestamp))
    fp.close()


def get_timestamp():
    
    with open ("timestamp", "r") as myfile:
        timestamp = myfile.readlines()
        myfile.close()
    
    print 'getting ', timestamp[0]
    return int(timestamp[0])
    # with open ("timestamp", "r") as fp:
    #     timestamp   =   fp.read()
    # print float(data)
    # return int(float(data))

save_timestamp()
get_timestamp()

@app.route('/')
def hello_world():
    return 'Hello sucka!'

@app.route('/play')
def play():
    call(['/var/www/htdocs/djface/shpotify-master/spotify', 'play'])
    return 'playing'

@app.route('/pause')
def pause():
    call(['/var/www/htdocs/djface/shpotify-master/spotify', 'pause'])
    return 'pausing playback'

@app.route('/next')
def next():

    if not os.path.isfile('timestamp'):
        save_timestamp()

    request_threashold = 10
    last_request = get_timestamp()

    print 'get timestamp: %s timetime: %s last_request: %s, math: %s' % (get_timestamp(), int(time.time()), last_request, (int(time.time()) - last_request))
    if request_threashold < (int(time.time()) - int(last_request)):
        save_timestamp()
        call(['/var/www/htdocs/djface/shpotify-master/spotify', 'next']) 
        return 'playing next track --  last rqeuest %s' % last_request 
    else:
        return "can't skip to next track.. threashold not met - %s" % (time.time() - last_request)
    # % (session['last_request'])

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0')
