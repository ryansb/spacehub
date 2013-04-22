from cornice import Service
from corniceapp.models import DBSession, Secret
from pyramid.httpexceptions import HTTPSeeOther, HTTPTemporaryRedirect
import requests
import logging
import urllib
import uuid

log = logging.getLogger('spacehub.oauth')

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API_URL = "https://api.github.com"
oauth = Service(name='oauth', path='/oauth', description="Service to deal with GitHub Oauth2 flow.")

@oauth.get()
def oauth_get_code(request):

    client_id = request.registry.settings["client_id"]
    client_secret = request.registry.settings["client_secret"]
    response = oauth_authorize(request)
    secret = None
    if DBSession.query(Secret).all().count > 0:
        secret = DBSession.query(Secret).first()
    else:
        secret = Secret()
    # do stuff to secret to set info
    secret.access_token = response.get('access_token')
    DBSession.add(secret)
    DBSession.commit()

    params = {
        "title": "Spacehub",
        "key": secret.public_key
    }

    # add public key to user's acc.
    requests.post(GITHUB_API_URL + "/user/keys", params=params)

    raise HTTPTemporaryRedirect(location="/app/index.html#/repos")

def oauth_authorize(request):
    """
    Use a previously received auth code or refresh token to get a new
    access token and refresh token if applicable.

    """

    params = {
        "client_id": request.registry.settings["client_id"],
        "client_secret": request.registry.settings["client_secret"],
        "code": request.params["code"]
    }
    headers = {
        "Accept": "application/json"
    }
    return requests.post(GITHUB_TOKEN_URL, params, headers=headers).json()

# FIrst
@oauth.post()
def outh_redirect(request):
    scopes = ['repo', 'notifications', 'gist', 'user']
    params = {
            "client_id": request.registry.settings["client_id"],
            # "client_secret": request.registry.settings["client_secret"],
            "scope": ','.join(scopes),
            #"state": str(uuid.uuid4())
    }

    raise HTTPSeeOther(location="%s?%s" % (GITHUB_AUTH_URL, urllib.urlencode(params)))

