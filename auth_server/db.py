import pymongo as Pymongo
import yaml as yaml

# constants 
CONFIG = "../config.yaml"
ENDPOINT = "mongodb+srv://%s:%s@cluster0-papif.mongodb.net/test?retryWrites=true"

# endregion init
class Driver():
    _client = None

    def __init__(self):
        with open(CONFIG) as f:
            # loads the username and password from yaml config file
            configMap = yaml.safe_load(f)
            user = configMap["secrets"]["mongoDB"]["user"]
            password = configMap["secrets"]["mongoDB"]["password"]
            
            print(ENDPOINT % (user, password))  
            self._client = Pymongo.MongoClient(ENDPOINT % (user, password))

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