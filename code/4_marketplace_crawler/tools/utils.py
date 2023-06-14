import time
import subprocess

# CHROME = ['google-chrome',
#           '--remote-debugging-port=9222',
#           '--allow-insecure-content',
#           '--start-fullscreen',
#           '--incognito']

#TODO a possible optimization is to list all 3rd party platforms
GAME_COLLECTIONS = [
                    'html5.gamedistribution.com',
                    'html5.iclouds.io',
                    'cdn2.addictinggames.com'
                    ]

#time intervals (set constants here)
TIMEOUT_MS = 120000 #total exp duration 2 mins
BUTTON_CLICK_MS = 30000 #0.5 secs
DISPATCH_EVENTS_AT_MS = 60000 #start injecting rnd clicks/keys #after one minute

#disabled error messages from chrome
def chrome_start(chrome_cmd):
    p = subprocess.Popen(chrome_cmd, stderr=subprocess.DEVNULL)
    return p

def chrome_stop(p):
    p.kill()

def get_chrome_port(chrome_cmd):
    return [x for x in chrome_cmd if "debugging-port" in x][0].split('=')[1]

def get_all(myjson):
    """ Recursively find all the values of key in all the dictionaries in myjson
        with a "type" key equal to kind.
    """
    if isinstance(myjson, dict):
        nodeId = myjson.get("nodeId", -1)  # -1 if key not present
        nodeName= myjson.get("nodeName", -1)
        attributes = myjson.get("attributes", -1)
        if nodeId!=-1 and nodeName!=-1 and attributes!=-1:
            yield {'nodeId':nodeId, 'nodeName':nodeName, 'attributes':attributes}
        for x in myjson:
            for v in get_all(myjson[x]):
                yield v #recursive
    elif isinstance(myjson, list):
        for item in myjson:
            for v in get_all(item):  # recursive
                yield v

def sanitize_url(url):
    #strip last / if any
    if url[-1]=='/':
        url=url[0:-1]
    #strip http:// or https://
    if url[0:8]=='https://':
        url = url[8:]
    if url[0:7]=='http://':
        url = url[7:]
    if url[0:2]=='//':
        url = url[2:]
    return url
