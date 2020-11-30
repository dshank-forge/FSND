import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt, exceptions
from urllib.request import urlopen

AUTH0_DOMAIN = 'goatpig.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'
CLIENT_SECRET = 'wsoGdfUUNJ2gW8PRUqfDTYksFdHPEkVHqjCuufsMHakgpM6WTBXQpA54RMkS1qoY'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

def get_token_auth_header():
    try:
        headers = request.headers
        auth_part = headers['Authorization']
        split_auth_part = auth_part.split()
        bearer = split_auth_part[0]
        token = split_auth_part[1]
    except Exception as e:
        raise AuthError(e, 401)
    return token

def check_permissions(permission, payload):
    try:
        permissions_array = payload['permissions']
        print('permission:' + str(permission))
        print('permissions array: ' + str(permissions_array))
        if permission not in permissions_array:
            'oops'
    except Exception as e:
        print('exception')
        raise AuthError(e, 401)
    return True

# The following function has been adapted from the Auth0 Docs - "Python API: Authorization" by Luciano Balmaceda
# URL: https://auth0.com/docs/quickstart/backend/python/01-authorization?_ga=2.212761047.219893380.1606509180-267051542.1604770864#create-the-jwt-validation-decorator
# Date: 11/29/2020

# ----- Begin Citation ----- # 

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

# ----- End Citation ----- # 

'''
@TODO implement verify_decode_jwt(token) method
    @DONE
        token: a json web token (string)

    the token should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''

def verify_decode_jwt(token):
    jwks_dictionary = json.loads(urlopen('https://'+AUTH0_DOMAIN+'/.well-known/jwks.json').read())
    
    try:
        verification_key = create_verification_key(jwks_dictionary, token)
    except Exception as e:
        raise AuthError(e, 401)

    try:
        payload = jwt.decode(token, verification_key, algorithms=ALGORITHMS, audience=API_AUDIENCE)
    except Exception as e:
        raise AuthError(e, 401)

    return payload



'''
@DONE implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method to validate claims and
    check the requested permission
    return the decorator which passes the decoded payload to the
    decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
