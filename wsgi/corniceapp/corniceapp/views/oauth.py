from cornice import Service
from cornice.models import DBSession, Secret
from pyramid.httpexceptions import HTTPTemporaryRedirect
import requests
import logging
import urllib
import uuid

log = logging.getLogger('spacehub.oauth')

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
oauth = Service(name='oauth', path='/oauth', description="Service to deal with GitHub Oauth2 flow.")

@oauth.get()
def oauth_get_code(request):
	response = oauth_authorize(request)
	secret = None
	if DBSession.get(Secret).all():
		secret = DBSession.get(Secret).all()[0]
	else:
		secret = Secret()
	# do stuff to secret to set info
	secret.access_token = response.access_token
	DBSession.add(secret)
	DBSession.commit()

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

@oauth.post()
def outh_redirect(request):
	scopes = ['repo', 'notifications', 'gist', 'user']
	params = {
			"client_id": request.registry.settings["client_id"],
			"client_secret": request.registry.settings["client_secret"],
			"scopes": ','.join(scopes),
			"state": str(uuid.uuid4())
	}

	raise HTTPTemporaryRedirect(location="%s?%s" % (GITHUB_AUTH_URL, urllib.urlencode(params)))

