""" Cornice services.
"""
from cornice import Service
from corniceapp.models import User, Repo, DBSession
from corniceapp.validators import validate_generic
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
)
from webob import Response
import hashlib
import json



watch_runner = Service(name="watch_runner", path="/watch_runner",
        description="Service to run the watcher for watched pages")

@watch_runner.get()
def get_watch_runner(request):
    """
        When GET'd to this, will get info on the running jorb
    """
    return ScrapeJob.all()

@watch_runner.post(validators=validate_generic)
def post_watch_runner(request):
    """
        When POSTED to this will start operating on watched pages
    """
    pass

@watch_runner.put()
def put_watch_runner(request):
    """
        Update the runner's status.
    """
    pass
