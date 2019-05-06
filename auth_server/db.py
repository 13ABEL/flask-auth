import pymongo

from . import config

# constants 
ENDPOINT = "mongodb+srv://%s:%s@cluster0-papif.mongodb.net/test?retryWrites=true"

# endregion init
class Driver():
    _client = None

    def __init__(self):
        self._client = pymongo.MongoClient(ENDPOINT % (config.USER, config.PASSWORD))

    def getClient(self):
        return self._client

if (__name__ == "__main__"): 
    driver = Driver()
    auth_db = driver.getClient()["auth_db"]
    auth_collection = auth_db["auth_collection"]
    data = {
        "client_id" : "test_client_id", 
        "auth_code" : "test_auth_code"
    }
    
    inserted_id = auth_collection.insert_one(data)
    print(inserted_id)