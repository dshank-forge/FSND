import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
AUTH0_DOMAIN = 'goatpig.us.auth0.com'
ALGORITHMS = ['RS256']
# API_AUDIENCE = 'dev'
API_AUDIENCE = 'coffee'

def verify_decode_jwt(token):
    content = urlopen('https://'+AUTH0_DOMAIN+'/.well-known/jwks.json')
    print(content)
    # raise Exception('Not Implemented')

verify_decode_jwt('hello')

https://goatpig.us.auth0.com/.well-known/jwks.json