import urllib.parse as UrlParser

from flask import *

PORT = 5001
TOKEN_TYPE = "JWT"

TOKEN_EXPIRY = "100"

app = Flask(__name__)

# authentication ->

# sign in page for user
@app.route("/auth")
def auth():
    # parse args from the url
    client_id = request.args.get("client_id")
    redirect_url = request.args.get("redirect_url")

    if (client_id == None or redirect_url == None):
        return json.dumps({
            "error" : "invalid request"
        }), 400

    # TODO check if access should be granted for client (assume it is for now just to get flow right)

    # need to pass client id & redirect url in b/c form needs it upon submission
    return render_template(
        "grant_access.html", 
        client_id = client_id,
        redirect_url = redirect_url
    )

# issues auth code after checking credentials
@app.route("/signin", methods = ["POST"])
def signin():
    username = request.form.get("username")
    password = request.form.get("password")
    client_id = request.form.get("client_id")
    redirect_url = request.form.get("redirect_url")

    if (None in [username, password, client_id, redirect_url]):
        return json.dumps({
            "error" : "invalid request"
        }), 400

    # TODO check if access should be granted for client (assume it is for now just to get flow right)
    # TODO check if user + pass is correct

    # generate auth code and stick it on to the redirect
    # TODO create method for generating auth code later
    auth_code = "TODO"
    new_redirect_url = consolidate_redirect(redirect_url, auth_code)

    # https://en.wikipedia.org/wiki/HTTP_303
    # indicates that we're redirecting to another uri
    return redirect(new_redirect_url, code = 303)

# accepts auth code and exchanges it for an access token
@app.route("/token", methods = ["POST"])
def exchange_auth():
    auth_code = request.form.get("authorization_code")
    client_id = request.form.get("client_id")
    client_secret = request.form.get("client_secret")
    redirect_url = request.form.get("redirect_url")

    if (None in [auth_code, client_id, client_secret, redirect_url]):
        return json.dumps({
            "error": "invalid request"
        }), 400
    
    # TODO check if client id & secret combo is valid
    # TODO check if auth code is valid

    # TODO create method for generating access token
    access_token = "test_access_token"

    # access token has three fields: actual token, type, expiry
    return json.dumps({
        "access_token": access_token,
        "token_type": TOKEN_TYPE,
        "expires_in": TOKEN_EXPIRY
    })



# region helpers

def consolidate_redirect(redirect_url, auth_code):
    # query args are stored in the fifth indice (named = "query")
    query_index = 4
    print(redirect_url)

    deconstructed_url = list(UrlParser.urlparse(redirect_url))
    queries = dict(UrlParser.parse_qsl(deconstructed_url[query_index]))
    # update auth code placeholder with actual auth code
    queries["authorization_code"] = auth_code

    # need to put everything back into place & "unparse" it
    deconstructed_url[query_index] = UrlParser.urlencode(queries)
    return UrlParser.urlunparse(deconstructed_url)


# endregion helpers

if __name__ == "__main__":
    app.run(port = PORT, debug = True)