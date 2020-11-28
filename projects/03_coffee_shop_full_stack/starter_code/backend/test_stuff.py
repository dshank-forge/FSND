import json
from flask import request, _request_ctx_stack
from functools import wraps
# from jose import jwt, exceptions
import jwt
from urllib.request import urlopen

# AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
AUTH0_DOMAIN = 'goatpig.us.auth0.com'
ALGORITHMS = 'RS256'
# API_AUDIENCE = 'dev'
API_AUDIENCE = 'coffee'
CLIENT_SECRET = 'wsoGdfUUNJ2gW8PRUqfDTYksFdHPEkVHqjCuufsMHakgpM6WTBXQpA54RMkS1qoY'


def verify_decode_jwt(token):
    # response = urlopen('https://'+AUTH0_DOMAIN+'/.well-known/jwks.json')
    # try:
    decoded_jwt = jwt.decode(token, CLIENT_SECRET, algorithms=['RS256'])
    print(decoded_jwt)
    # except Exception:
    #     print('dependency error')


mytoken = b'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IndoMXVtVkZzZ0pUZzNEc1dZcU55NyJ9.eyJpc3MiOiJodHRwczovL2dvYXRwaWcudXMuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE1MjAyNjQwNzQ2ODAxMDAwODkwIiwiYXVkIjpbImNvZmZlZSIsImh0dHBzOi8vZ29hdHBpZy51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA1NDkxMTYzLCJleHAiOjE2MDU0OTgzNjMsImF6cCI6ImwyaU5Hb2pZbXQyazkxVXlmdzJidXhaanJrbEFMMFI4Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbXX0.mFGOq6czt9lSlKFG_wR5IwJm_lcY7cgRkmYgcKCBfQPlsbFbRleTkBdGBaqfc4c6AL1rdGhNQBOKrAXBNGdvQFxfVHYaUceNK-JFPzlHa2Whbu_ZgwupLD5kxgWHSzZcnwU_rXU93DIxsqiZLvG7LFm0fk7QPA7j7UiKPrNaGhsGT9VewzGraAMBwc84q_71NJ3W7w5ccI_EJ_nBYhxu2QxDiMfSWLvis4-_XQvE9Xg4qzDzU2aBhnFLCbf-AodnEYxpB8k9o4Jbv0MCK7KqJDGTvlSMH8vhQsNDhixr9OmCnBhUs_Of1t0oKaU9VFQn1NA78j2e-WKr2u7uTQjA-w'

# verify_decode_jwt(mytoken)
# I get an error that the RSA key format is not supported. Maybe this is because my pycryptodome or
# whatever failed to install correctly.

# https://goatpig.us.auth0.com/.well-known/jwks.json

encoded_token = jwt.encode(
    {'some': 'payload'}, CLIENT_SECRET, algorithm='RS256')
print(encoded_token)

# decoded_token = jwt.decode(mytoken, CLIENT_SECRET, algorithms=['RS256'])
# print(decoded_token)
