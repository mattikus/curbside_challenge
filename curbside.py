#!/usr/bin/env python3
""" Just a simple solution to the challenge over at
http://challenge.shopcurbside.com/ using python 3.3+ and fun things like
generators and decorators, because why the hell not. """

from functools import wraps
import requests

def memo_limit(func):
    """ memoize the results of a function up to 10 times """
    uses = 10
    data = None

    @wraps(func)
    def call_func():
        nonlocal data, uses
        if not data or uses < 1:
            data = func()
            uses = 10
        uses -= 1
        return data
    return call_func

@memo_limit
def get_session():
    """ Get a new session token from the challenge """
    return requests.get("http://challenge.shopcurbside.com/get-session").text

def walk(id):
    """ Do a basic depth-first traversal of the tree """
    req = requests.get("http://challenge.shopcurbside.com/{0}".format(id),
                       headers={'Session': get_session()})

    data = req.json()

    if 'secret' in data:
        yield data['secret']

    # Sometimes keys show up in crazy capitalization, normalize
    data = {k.lower(): v for k, v in data.items()}

    if 'next' not in data:
        return

    # Apparently the json will return a single string instead of a list of
    # strings occasionally, check for it and fix
    if isinstance(data['next'], str):
        data['next'] = [data['next']]

    for id in data['next']:
        yield from walk(id)

if __name__ == "__main__":
    print(''.join(x for x in walk('start')))
