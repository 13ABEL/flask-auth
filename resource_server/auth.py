import jwt

from . import config

def verify_access_token(jw_token ):
    config.PUBLIC_KEY

    try:
        print(jwt)
        payload = jwt.decode(jw_token, config.PUBLIC_KEY, issuer = config.ISSUER, algorithm = config.ENCRYPT_ALGO)
        print(payload)
    
    except(
        jwt.exceptions.ExpiredSignature, 
        jwt.exceptions.InvalidIssuerError, 
        jwt.exceptions.InvalidTokenError
        ) as e:

        print(f"issue decoding token {e}")
        return False        
    
    return True

