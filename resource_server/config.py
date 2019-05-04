ISSUER = "example_auth_server"
PORT = 5002

ENCRYPT_ALGO = "RS256"

# secrets that need to be kept separate from the main file
PUBLIC_KEY = None

PATH_PUBLIC_KEY = "public.pem"

config_vals = ["public.pem"]

with open (PATH_PUBLIC_KEY) as public_key_f:
    PUBLIC_KEY = public_key_f.read()
    if (PUBLIC_KEY == None): 
        raise(Exception("Missing public.pem"))

if __name__ == "__main__":
    i = 0
    for config_value in [PUBLIC_KEY]:
        print(f"{config_vals[i]} = {config_value}")
        i += 1 