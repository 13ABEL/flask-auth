import base64
import string
import jwt
import random
import time

from . import (config, db)

driver = db.Driver()

def generate_auth_code(client_id, subject):
    auth_code = ""
    # we can use any randomly generated string
    for i in range(10):
        auth_code += random.choice(string.ascii_letters)
    
    # store auth code in db
    # need to "register" the auth code with the username for access
    auth_collection = driver.getClient()["auth_db"]["auth_coll"]
    doc = {
        "_id" : client_id, 
        "auth_code" : auth_code, 
        "subject" : subject
        }
    auth_collection.save(doc)

    return auth_code

def check_auth_code(client_id, auth_code):
    # store auth code in db
    auth_collection = driver.getClient()["auth_db"]["auth_coll"]

    query = { "_id" : client_id }
    query_docs = auth_collection.find(query)

    if (query_docs.count() == 0):
        return False
    
    # check if auth code matches the one stored in db
    for query_doc in query_docs:
        print("compare auth codes")
        print(query_doc["auth_code"])
        print(auth_code )

        if (query_doc["auth_code"] != auth_code):
            return False

    return True

def get_username(auth_code):
    auth_collection = driver.getClient()["auth_db"]["auth_coll"]

    query = { "auth_code" : auth_code }

    query_docs = auth_collection.find(query)

    if (query_docs.count() == 0):
        return None

    return query_docs[0]["subject"]

def generate_access_token(username):
    # the example repo I followed uses jwt for the access token
    # I decided to stick with it because our resource server is separate from our authentication server
    payload = {
        "iss" : config.ISSUER,
        "exp" : time.time() + config.TOKEN_EXPIRY,
        "sub" : username,

    }
    
    return jwt.encode(payload, config.PRIVATE_KEY, algorithm = config.ENCRYPT_ALGO)