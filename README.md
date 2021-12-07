# toke
A simple CLI that does the code exchange flow for OAuth.
Handy when trying to get a user token to debug things.

## Setup

The usual python virtual environments apply. Create one by following the steps here

```shell
  python3 -m venv toke
  pip install -r requirements.txt
```

Usage:

 python index.py <CLIENT_ID> <CLIENT_SECRET> <LIST_OF_SCOPES_COMMA_SEPARTED> <REDIRECT_URI> <OAUTH_SERVER_BASE>
