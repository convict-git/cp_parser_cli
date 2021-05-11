import os
from os.path import expanduser
import sys
from signal import signal, SIGINT
from sys import exit
import requests
import click
import time
from playsound import playsound

home_dir=expanduser("~")
sound=[home_dir+'/AC-Sound.mp3', home_dir+'/WA-Sound.mp3']
username = ""
pretty_username=""

wait="←↖↑↗→↘↓↙"
wait_idx=0
last_verdict=""
verdict_stack=""
colors = {'newbie':'\033[37m', 'pupil':'\033[32m', 'specialist':'\033[36m',
        'expert':'\033[34m', 'candidate master':'\033[35m', 'master':'\033[93m',
        'international master':'\033[93m', 'grandmaster':'\033[91m',
        'international grandmaster':'\033[91m', 'legendary grandmaster':'\033[91m'}

def handler(signal_received, frame):
    print('\n\t\033[92;1;7m  Good bye!  \033[0m')
    os._exit(os.EX_OK)

def safeget(dct, key):
    try:
        dct = dct[key]
    except KeyError:
        return None
    return dct

def get_rank_rating(user):
    r = requests.get('https://codeforces.com/api/user.info?handles={0}'.format(user))
    js = r.json()
    if 'status' not in js or js['status'] != 'OK':
        raise ConnectionError('Cannot connect to codeforces!')
    else:
        try:
            rank = js['result'][0]['rank']
            rating = js['result'][0]['maxRating']
        except Exception as e: # rating is 0 (new user)
            return '\033[1m{} Unrated 0\033[0m'.format(user)
        return '\033[1m{} {} {} {}\033[0m'.format(colors[rank], user, rating, rank)

def get_last_verdict(user):
    r = requests.get('http://codeforces.com/api/user.status?' +
                     'handle={}&from=1&count=1'.format(user))
    js = r.json()
    if 'status' not in js or js['status'] != 'OK':
        return False, 0, 0, 0, 0, 0, 0, 0
        # raise ConnectionError('Cannot connect to codeforces!')
    try:
        result = js['result'][0]
        id_ = result['id']
        verdict_ = safeget(result, 'verdict')
        time_ = result['timeConsumedMillis']
        memory_ = result['memoryConsumedBytes'] / 1000
        passedTestCount_ = result['passedTestCount']
        problem_ = result['problem']
        contestId_ = problem_['contestId']
        problemIndex_ = problem_['index']
    except Exception as e:
        return False, 0, 0, 0, 0, 0, 0, 0
        # raise ConnectionError('Cannot get latest submission, error')
    return True, id_, verdict_, time_, memory_, passedTestCount_, contestId_, problemIndex_

def get_time():
    return "\033[7m[ " + time.strftime("%H:%M:%S", time.localtime()) + " ]\033[0m"

def run():
    global wait_idx, last_verdict, verdict_stack
    got, last_id, _, _, _, _, _, _ = get_last_verdict(username)
    if (got == False):
        print('\033[91;1m Some error occurred\033[0m')
        time.sleep(1)
        run()

    hasStarted = False
    while True:
        wait_idx += 1
        wait_idx %= len(wait)
        if (not hasStarted):
            os.system('clear')
            print('{}\n{} {}\nWaiting for a {}\'s submission... \033[1;7m {} \033[0m'.format(verdict_stack, get_time(), pretty_username, username, wait[wait_idx]))

        got, id_, verdict_, time_, memory_, passedTestCount_, contestId_, problemIndex_  = get_last_verdict(username)

        if (got == False):
            print('\033[91;1m Some error occurred\033[0m')
            time.sleep(1)
            continue
        if id_ != last_id:
            os.system('clear')
            result=-1
            if (verdict_ == None or verdict_ == 'TESTING'):
                if (not hasStarted):
                    last_verdict = '\033[92m Received a submission for {} {}... \033[1m{}\033[0m'.format(contestId_, problemIndex_, wait[wait_idx])
                    hasStarted = True
                else:
                    last_verdict=' \033[93;1mTesting \033[7m {} \033[0m\033[93m {} {}\033[0m'.format(wait[wait_idx], contestId_, problemIndex_)

            else:
                if verdict_ == 'OK':
                    last_verdict=' \033[92;1m✓ \033[7m Accepted \033[0m\033[92m  {} {} Passed {} tests \n\t{} MS | {} KB \033[0m'.format(contestId_, problemIndex_, passedTestCount_, time_, memory_)
                    result=0
                else:
                    last_verdict=' \033[91;1m✗ \033[7m {} \033[0m\033[91m - {} {} on test {} \n\t{} MS | {} KB \033[0m'.format(verdict_, contestId_, problemIndex_, passedTestCount_+1, time_, memory_)
                    result=1

            print(last_verdict)
            if result != -1:
                verdict_stack += "\n" + get_time() + "\n\n" + last_verdict + "\n"
                playsound(sound[result])
                last_id = id_
                hasStarted = False
                time.sleep(10)

            time.sleep(0.2)
        else:
            time.sleep(1)

signal(SIGINT, handler)
if (len(sys.argv) == 1):
    print('Please provide username as arugment (in quotes)')
else:
    username=sys.argv[1]
    pretty_username=get_rank_rating(username)
    run()
