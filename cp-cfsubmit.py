import os
import socket
import requests
import stdiomask
import time
import json
from signal import signal, SIGINT
from sys import exit
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser


######################### Some global constants ################################################

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 8889
sessionUser = 'guest'
failedAttempt = False
# Color organiser for logs
co = {
        'fr': "\33[0m\33[31m", 'fg': "\33[0m\33[32m", 'fy': "\33[0m\33[33m",
        'bg': "\33[0m\33[42m", 'br': "\33[0m\33[41m",
        'r' : "\33[0m"
        }
########################## Some helper methods #################################################


# Logger method
def logger (type, message):
    """This is logger method to log messages based on type
    error, warning or success (or info)"""
    msg=""
    if (type == "error"):
        msg += co['fr']
    elif (type == "warning"):
        msg += co['fy']
    elif (type == "success"):
        msg += co['fg']
    else:
        msg += ""
    msg += "[  " + time.strftime("%H:%M:%S", time.localtime()) + ' - ' + sessionUser + " ] : "
    print(msg + message + co['r'])

# To safely access map
def safeget(dct, key):
    try:
        dct = dct[key]
    except KeyError:
        return None
    return dct

# To convert list to str
def list_to_str(l):
    return '(' + ', '.join([str(el) for el in l]) + ')'

# To exit gracefully
def handler(signal_received, frame):
    logger ('success', 'SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

################################################################################################

def login_console():
    """login_console takes no argument and returns a pair of strings (username and password )"""

    global failedAttempt
    if (failedAttempt == True):
        logger('error', 'Previous login attempt failed')
    logger("info", "Waiting for details to signin")

    # The below code looks ugly because it intends to make things look beautiful at CLI
    print(co['bg'] + "   Login into \33[47m📊                \33[1m\33[30mCODE\33[34mFORCES  " + co['r'])
    print(co['bg'] + " " + co['r'] + co['fg'] + "\t username : " + co['r'], end=' ', flush=True)
    username = input("\33[4m")
    print(co['bg'] + " " + co['r'] + co['fg'] + "\t password : " + co['r'], end=' ', flush=True)

    # Taking password using stiomask to hide it under asterisk (*)
    password = stdiomask.getpass(prompt="\33[4m")
    print(co['r'] + co['bg'] + "         " + co['r'])

    return (username, password)

################################################################################################

def login_to_cf(username, password):
    """login_to_cf creates a codeforces logged in session using RoboBrowser"""

    logger ('info', 'Trying to login into codeforces for the handle : {0}'.format(username))

    try:
        browser = RoboBrowser(parser = 'html.parser')
        browser.open('http://codeforces.com/enter')

        enter_form = browser.get_form('enterForm')
        enter_form['handleOrEmail'] = username
        enter_form['password'] = password
        browser.submit_form(enter_form)

        checks = str(browser.select('div.caption.titled')).count(username)
        if checks == 0 or username == "":
            logger ('error', 'Login Failed.. Wrong password.')
            return (False, browser)
    except Exception as e:
        logger('error', 'Login Failed.. Maybe wrong id/password.')
        return (False, browser)

    global sessionUser
    sessionUser = username
    logger ('success', 'Login successful, Welcome {0}!'.format(sessionUser))
    return (True, browser)

################################################################################################

def submit_to_cf(browser, contestId, problemIndex, filename):
    """submit_to_cf submits a solution to the given contestId/problemIndex as file using
    logged in browser session"""

    logger ('info', 'Trying to submit')

    try:
        browser.open('https://codeforces.com/contest/{0}/submit/{1}'.format(contestId, problemIndex))
        submit_form = browser.get_form(class_ = 'submit-form')
        submit_form['sourceFile'] = filename
    except Exception as e:
        logger ('error', 'File {0} not found'.format(filename))
        return False
    browser.submit_form(submit_form)
    if (browser.url.count('token') > 0):
        logger ('error', 'Same file submitted before')
        return False
    return True

################################################################################################

def validate_cf_url(url):
    urlList = url.split("/")
    (cType, contestId, pType, problemIndex) = urlList[-4:]
    if (url.count('codeforces') == 0 or cType != 'contest' or pType != 'problem'):
        return (False, "", "")
    return (True, contestId, problemIndex)

################################################################################################

def main():
    global failedAttempt
    os.system('clear')
    # Show login screen
    username, password = login_console()
    # Create a RoboBrowser login session using the received credentials
    (isLoggedIn, browser) = login_to_cf(username, password)
    if (isLoggedIn == False):
        failedAttempt = True
        main()

    # UDP server initialization
    logger ("info", "Initializing UDP server listening on {}:{}".format(UDP_IP_ADDRESS, UDP_PORT_NO))
    try:
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    except Exception as e:
        logger ("error", "Unable to setup the server at port")
        return

    logger ("success", "Successfully created a server at {}:{}".format(UDP_IP_ADDRESS, UDP_PORT_NO))

    # Listen all the while
    while(True):
        logger ("warning", "listening for json data on {}".format(UDP_PORT_NO))

        # recv data from a UDP client
        try:
            data, addr = serverSock.recvfrom(1024)
        except Exception as e:
            logger ("error", "Some error occurred while receiving")

        logger ("success", "recv from " + str(addr[0]) + ':' +  str(addr[1]))

        # Expected json (minimum requirements)
        # eg.
        # {
        # "filename":"/home/user/.../main.cpp",
        # "pconfig":{"url":"https://codeforces.com/contest/1475/problem/A"}
        # }
        js = json.loads(data.decode('utf-8'))
        filename = js['filename']
        cpplabel = filename.split('/')[-1]
        url = safeget(js['pconfig'], 'url')
        if (url == None):
            logger ('error', 'This problem was parsed by a previous version of cp-parser-cli')
            continue

        url = js['pconfig']['url']
        isValid, contestId, problemIndex = validate_cf_url(url)

        if (isValid == True): # True for all cf problems (except gym)
            logger('success', 'Valid URL for codeforces found')
            if (submit_to_cf(browser, contestId, problemIndex, filename)):
                logger('success', 'Submitted {2} successfully for {0}/{1}'.format(contestId, problemIndex, cpplabel))
            else:
                logger('error', 'Failed at submitting {2} for {0}/{1}'.format(contestId, problemIndex, cpplabel))
        else:
            logger('error', 'This is not a valid codeforces problem')

################################################################################################

if __name__ == "__main__":
    signal(SIGINT, handler)
    logger("success", "Welcome to cp-cfsubmit")
    main()
