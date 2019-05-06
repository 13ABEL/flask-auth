import base64
import string
import jwt
import random
import time

from . import (config, db)

driver = db.Driver()

def generate_auth_code(client_id):
    auth_code = ""
    # we can use any randomly generated string
    for i in range(10):
        auth_code += random.choice(string.ascii_letters)
    
    # store auth code in db
    auth_collection = driver.getClient()["auth_db"]["auth_coll"]
    doc = {
        "_id" : client_id, 
        "auth_code" : auth_code
        }
    auth_collection.save(doc)

    return auth_code

def check_auth_code(client_id, auth_code):
    # store auth code in db
    auth_collection = driver.getClient()["auth_db"]["auth_coll"]

    query = { "_id" : client_id }
    query_docs = auth_collection.find(query)

    if (query_docs.__sizeof__ == 0):
        return False
    
    # check if auth code matches the one stored in db
    for query_doc in query_docs:
        print("compare auth codes")
        print(query_doc["auth_code"])
        print(auth_code )

        if (query_doc["auth_code"] != auth_code):
            return False

    return True

def generate_access_token():
    # the example repo I followed uses jwt for the access token
    # I decided to stick with it because our resource server is separate from our authentication server
    payload = {
        "iss" : config.ISSUER,
        "exp" : time.time() + config.TOKEN_EXPIRY
    }
    
    return jwt.encode(payload, config.PRIVATE_KEY, algorithm = config.ENCRYPT_ALGO)