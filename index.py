import base64
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
import requests
import json
import argparse
from urllib.parse import urlparse

CLIENT_ID = ""
CLIENT_SECRET = ""
SCOPES = ""
REDIRECT_URI = ""
AUTH_SERVER = ""


def get_auth_code():
    AUTHORIZATION_URL = AUTH_SERVER + "/authorize?response_type=code&client_id={client_id}&scopes={scopes}&redirect_uri={redirect_uri}".format(
        client_id=CLIENT_ID, scopes=SCOPES, redirect_uri=REDIRECT_URI)

    webbrowser.open(AUTHORIZATION_URL)


def extract_auth_code(request: str):
    return request.split("?code=")[1]


def exchange_code_for_token(auth_code):
    header = base64.b64encode(
        bytes(CLIENT_ID + ":" + CLIENT_SECRET, "utf-8")).decode("ascii")

    auth_data = {
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(AUTH_SERVER + "/api/token", headers={
        "Authorization": "Basic " + header
    }, data=auth_data)

    return response.json()


class AuthCodeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth_code = extract_auth_code(self.path)
        access_token = exchange_code_for_token(auth_code)
        self.respond_to_browser(access_token)
        print(json.dumps(access_token, indent=4))

    def log_message(self, format, *args):
        return

    def respond_to_browser(self, access_token):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>Get Token</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(
            bytes("<p>Access Token: </p> <br/> {token}".format(
                token=json.dumps(access_token, indent=4)), "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get a User Access Token via Oauth 2')
    parser.add_argument('client_id', metavar='CLIENT_ID', type=str,
                        help='The Client ID for the Oauth App')
    parser.add_argument('client_secret', metavar='CLIENT_SECRET', type=str,
                        help='The Client Secret for the Oauth App')
    parser.add_argument('scopes', metavar='SCOPES', type=str,
                        help='Requested scopes \',\' delimited for the access token')
    parser.add_argument('redirect_uri', metavar='REDIRECT_URI', type=str,
                        help='The Redirect URI for the Oauth App - Has to be a local host one')
    parser.add_argument('oauth_host', metavar='OAUTH_HOST', type=str,
                        help='The server which supports the oauth flow')

    args = parser.parse_args()
    CLIENT_ID = args.client_id
    CLIENT_SECRET = args.client_secret
    SCOPES = args.scopes
    REDIRECT_URI = args.redirect_uri
    AUTH_SERVER = args.oauth_host
    PARSED_URI = urlparse(REDIRECT_URI)

    if (PARSED_URI.hostname != "localhost"):
        sys.exit(
            "Redirect URI has to be a localhost one - Found  " + PARSED_URI.hostname)

    webServer = HTTPServer((PARSED_URI.hostname, PARSED_URI.port),
                           AuthCodeHandler)

    try:
        get_auth_code()
        webServer.handle_request()
    except KeyboardInterrupt:
        pass
    finally:
        webServer.server_close()
