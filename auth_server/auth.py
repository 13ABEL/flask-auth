import base64
import string as String
import jwt as JWT
import random as Random
import time as Time

import config as Config
import db as DB_layer

driver = DB_layer.Driver()

def generate_auth_code(client_id):
    auth_code = ""
    # we can use any randomly generated string
    for i in range(10):
        auth_code += Random.choice(String.ascii_letters)
    
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
        "iss" : Config.ISSUER,
        "exp" : Time.time() + Config.TOKEN_EXPIRY
    }
    
    return JWT.encode(payload, Config.PRIVATE_KEY, algorithm = Config.ENCRYPT_ALGO)