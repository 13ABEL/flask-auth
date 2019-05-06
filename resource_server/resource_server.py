from flask import *

from . import (auth, config)

app = Flask(__name__)

# register this to run before every request -> checks token
@app.before_request
def before_request():
    auth_header = request.headers.get("Authorization")

    if (auth_header[0:7] != "Bearer "):
        return json.dumps({
            "error" : "Access token not included in request"
        }), 400
    
    access_token = auth_header[len("Bearer "):]

    if (auth.verify_access_token(access_token) == False):
        return json.dumps({
            "error" : "Access token is invalid"
        }), 400


@app.route("/current_user", methods = ["GET"])
def current_user():
    user_id = request.args.get("user_id")

    if (user_id == None):
        return json.dumps({
            "error" : "no user id specified for request"
        }), 400

    # replace with db call later
    return json.dumps({
        "user" : {
            "first_name" : "richard",
            "last_name" : "wei"
        }
    })    
    

if __name__ == "__main__":
    app.run(port = config.PORT, debug = True)