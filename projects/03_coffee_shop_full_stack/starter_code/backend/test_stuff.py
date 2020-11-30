import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt, exceptions
# import jwt
# from cryptography.x509 import load_pem_x509_certificate
# from cryptography.hazmat.backends import default_backend
from urllib.request import urlopen

# AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
AUTH0_DOMAIN = 'goatpig.us.auth0.com'
ALGORITHMS = 'RS256'
# API_AUDIENCE = 'dev'
API_AUDIENCE = 'coffee'
CLIENT_SECRET = 'wsoGdfUUNJ2gW8PRUqfDTYksFdHPEkVHqjCuufsMHakgpM6WTBXQpA54RMkS1qoY'





mytoken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IndoMXVtVkZzZ0pUZzNEc1dZcU55NyJ9.eyJpc3MiOiJodHRwczovL2dvYXRwaWcudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmYzQxMzkzMGJkNGMyMDA2OGY2ZjQ4NiIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTYwNjY4NTYwNCwiZXhwIjoxNjA2NjkyODA0LCJhenAiOiJsMmlOR29qWW10Mms5MVV5ZncyYnV4Wmpya2xBTDBSOCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.FfvIUiR0issWbF-bB20gb_3mKUamu_JRw-6_PXyn3AdumJ0QEwbfL4vP3WDsjdocToEj9D-D-adlIfJgPeJbSDLfyypq-xWOKRLJewshC57QQwNneyctUqo39cz2wmMknHDNmc-tjSl3cXvnUiaPv7vP6GNBvUXeVGalFsKLkqMwAvJ9wHc5kjqTwQxYiLyAHH22Nn9Df7Wt8MJA2Q5LfME8US4VoGZyhlOG4AmQ1ajwhiutdwuZuMn1vCMwit_fa3vwpXLmP2CKfOjxeOLxeJAmHZFovqisEbKgoAprrPFvosRcpiLHABWW2DEXoq1waHWLBOcZFetTQ6kL3G8TLQ'


# https://goatpig.us.auth0.com/.well-known/jwks.json

# The following function has been adapted from the Auth0 Docs - "Python API: Authorization" by Luciano Balmaceda
# URL: https://auth0.com/docs/quickstart/backend/python/01-authorization?_ga=2.212761047.219893380.1606509180-267051542.1604770864#create-the-jwt-validation-decorator
# Date: 11/29/2020
# start citation ---

def create_verification_key(jwks_dict, token):
    unverified_header = jwt.get_unverified_header(token)

    for key in jwks_dict["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
            break 

    return rsa_key

# end citation ---

# @TODO implement verify_decode_jwt(token) method
#     @DONE
#         token: a json web token (string)

#     the token should be an Auth0 token with key id (kid)
#     it should verify the token using Auth0 /.well-known/jwks.json
#     it should decode the payload from the token
#     return the decoded payload

def verify_decode_jwt(token):
    jwks_dictionary = json.loads(urlopen('https://'+AUTH0_DOMAIN+'/.well-known/jwks.json').read())
    verification_key = create_verification_key(jwks_dictionary, token)
    
    try:
        payload = jwt.decode(token, verification_key, algorithms=ALGORITHMS, audience=API_AUDIENCE)
    except Exception as e:
        print(e)

    return payload

payload = verify_decode_jwt('aljksdlkj.ssss.sss')
print(payload)