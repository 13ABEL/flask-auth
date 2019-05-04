import yaml as yaml

# const. that can be exposed publicly
ISSUER = "example_auth_server"
PORT = 5001

JWT_LIFESPAN = 100
TOKEN_EXPIRY = JWT_LIFESPAN
ENCRYPT_ALGO = "RS256"

# path to config file
PATH_CONFIG = "config.yaml"
PATH_PRIVATE_KEY = "private.pem"

# secrets that need to be kept separate from the main file
USER = None
PASSWORD = None
PRIVATE_KEY = None

config_vals = ["secrets.mongoDB.user", "secrets.mongoDB.password", "private.pem"]

with open(PATH_CONFIG) as f:
    # loads the username and password from yaml config file
    configMap = yaml.safe_load(f)
    USER = configMap["secrets"]["mongoDB"]["user"]    
    PASSWORD = configMap["secrets"]["mongoDB"]["password"]

    i = 0
    for config_value in [USER, PASSWORD]:
        if (config_value == None):
            missing_path = config_vals[0]
            raise(Exception(f"Missing '{missing_path}' entry in config file"))
        i += 1 

with open (PATH_PRIVATE_KEY) as private_key_f:
    PRIVATE_KEY = private_key_f.read()
    if (PRIVATE_KEY == None): 
        raise(Exception("Missing private.pem"))

if __name__ == "__main__":
    i = 0
    for config_value in [USER, PASSWORD, PRIVATE_KEY]:
        print(f"{config_vals[i]} = {config_value}")
        i += 1 