# toke
A simple CLI that does the code exchange flow for OAuth.
Handy when trying to get a user token to debug things.

## Setup

The usual python virtual environments apply. Create one by following the steps here

```shell
  python3 -m venv toke
  pip install -r requirements.txt
```


# How it works

This scripts starts a SimpleHttpServer instance on localhost and the port that's mentioned
in the redirect url. The redirect_uri needs to be registered before hand with the oauth app.


It will then initiate an authorization code request to the oauth server by opening up the defualt webbrowser for the system.

Once you've consented the app to get the required details from the server, the script will listen to the redirect_url that the oauth server will send the user to once
the credentials have been verified.

The script then issues a token request and prints it on the CLI as well as the web browser.

Nothing hacky, simple oauth without setting up a heavy weight app to do this.


## Usage:

```shell
 python index.py <CLIENT_ID> <CLIENT_SECRET> <LIST_OF_SCOPES_COMMA_SEPARTED> <REDIRECT_URI> <OAUTH_SERVER_BASE>
```
