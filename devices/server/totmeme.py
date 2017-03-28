#!/usr/bin/python3
import requests
import datetime
import time

def ping(addr='https://totmeme-161806.appspot.com/callback?action=server&name=server'):
    try:
        r = requests.get(addr)
        text = r.text
        r.close()
        if text != 'OK':
            print('GOT ANSWER: ' + text + ' AT ' + str(datetime.datetime.now()))
    except Exception as e:
        print('Cannot connect: ' + str(e))

def main(interval=120):
    while True:
        ping()
        time.sleep(interval)

if __name__ == '__main__':
    main()