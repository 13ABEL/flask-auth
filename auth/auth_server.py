import urllib.parse as UrlParser
from flask import *

PORT = 5001

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