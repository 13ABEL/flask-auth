import jwt as JWT

import config as Config


def verify_access_token(jwt):
    Config.PUBLIC_KEY

    try:
        print(jwt)
        payload = JWT.decode(jwt, Config.PUBLIC_KEY, issuer = Config.ISSUER, algorithm = Config.ENCRYPT_ALGO, options={'verify_aud': False})
        print(payload)
    
    except(
        JWT.exceptions.ExpiredSignature, 
        JWT.exceptions.InvalidIssuerError, 
        JWT.exceptions.InvalidTokenError
        ) as e:

        print(f"issue decoding token {e}")
        return False        
    
    return True

