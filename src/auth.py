import pymongo as pymongo
import yaml as yaml

# constants 
CONFIG = "../config.yaml"
ENDPOINT = "mongodb+srv://%s:%s@cluster0-papif.mongodb.net/test?retryWrites=true"

def connect():
    with open(CONFIG) as f:
        # loads the username and password from yaml config file
        configMap = yaml.safe_load(f)
        user = configMap["secrets"]["mongoDB"]["user"]
        password = configMap["secrets"]["mongoDB"]["password"]
        
        print(ENDPOINT % (user, password))
        client = pymongo.MongoClient(ENDPOINT % (user, password))
        db = client.test

if (__name__ == "__main__"): 
        print("test")  
        connect()