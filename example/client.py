import requests

from flask import (
    Flask, 
    request,
    render_template,
    json,
    make_response,
    redirect,
    url_for
)

CLIENT_ID = "example_client_id"
CLIENT_SECRET = "example_client_secret"

PORT = 5000
AUTH_SERVER = "http://localhost:5001"
RES_SERVER = "http://localhost:5002"

AUTH_URL = f"{AUTH_SERVER}/auth"
TOKEN_URL = f"{AUTH_SERVER}/token"
REDIRECT_URL = f"http://localhost:{PORT}/callback"

app = Flask(__name__)

@app.route("/login")
def login():
    # generate the redirect url here
    auth_link = f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_url={REDIRECT_URL}"
    # generates full redirect url:
    # http://localhost:5001/auth?response_type=code&client_id=example-client-id&redirect_url=http://localhost:5000/callback
    return render_template("login.html", authorization_link = auth_link)

# callback -> where the user is sent after authentication
# this is where we need to extract the auth code (obtained when user logs in)
@app.route("/callback")
def callback():
    auth_code = request.args.get("authorization_code")

    if (auth_code == None):
        return json.dumps({
            "error" : "no authorization code received"
        }), 500

    # TODO implement exchange in authorization server
    # exchange auth code for token
    result = requests.post(TOKEN_URL, data = {
        "grant_type": "authorization_code",
        "authorization_code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_url": REDIRECT_URL
    })

    if (result.status_code != 200):
        return json.dumps({
            "error" : f"failed to exchange auth code for access token \n{result.text}"
        }), 500

    access_token = json.loads(result.text).get("access_token")

    # redirect to main and store token as cookie
    response = make_response(redirect(url_for("main")))
    response.set_cookie("access_token", access_token)
    return response

# placeholder for the "real" site after authentication
@app.route("/")
def main():
    user_id = 10001
    access_token = request.cookies.get("access_token")
    
    # todo make request for actual data from resource server w/ token
    result = requests.get(RES_SERVER + f"/current_user?user_id={user_id}", headers = {
        "Authorization" : f"Bearer {access_token}"
    })

    if (result.status_code != 200):
        return json.dumps({
            "error" : f"issue retrieving resource {result.text}"
        }), 500

    user = json.loads(result.text).get("user")
    if (user == None):
        return json.dumps({
                "error" : f"doesn't look like a user with id '{user_id}' exists"
        }), 400

    return render_template("main.html", user = user)

if __name__ == "__main__":
    app.run(port = PORT, debug = True)