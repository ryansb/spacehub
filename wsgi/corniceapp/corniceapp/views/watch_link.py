""" Cornice services.
"""
from cornice import Service
from corniceapp.models import User, DBSession
from corniceapp.validators import validate_generic
from pyramid.security import (
    authenticated_userid,
)
from webob import Response
import hashlib
import json


watch_page = Service(name="watch_page", path="/watch_page",
        description="Service to deal with watching page links for changed files")

@watch_page.get(validators=validate_generic)
def get_watched_page(request):
    """
        Get all trackedlinks that spacehub knows of for the user
    """
    current_user = DBSession.query(User).filter(
        User.email == authenicated_userid(request)).one()

    filtered_tracks = []
    for repo in current_user.repos:
        t_link = repo.track_link
        if t_link:
            filtered_tracks.append(t_link.to_dict())

    return {"tracked_links": filtered_links}

@watch_page.put(validators=validate_generic)
def put_watched_page(request):
    """
        Edit watched page
    """
    pass

@watch_page.post(validators=validate_generic)
def post_watched_page(request):
    """
        Add a new watched page
    """
    pass
