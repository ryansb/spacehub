""" Cornice services.
"""
from cornice import Service
from spacehub.models import User, TrackedLink, DBSession
from spacehub.validators import validate_generic
from pyramid.security import (
    authenticated_userid,
)


watch_page = Service(name="watch_page", path="/watch_page",
        description="Service to deal with watching page links for changed files")

@watch_page.get()
def get_watched_page(request):
    """
        Get all trackedlinks that spacehub knows of for the user
    """
    current_user = DBSession.query(User).filter(
        User.email == authenticated_userid(request)).one()

    filtered_tracks = []
    for repo in current_user.repos:
        t_link = repo.track_link
        if t_link:
            filtered_tracks.append(t_link.to_dict())

    return {"tracked_links": filtered_tracks}

@watch_page.put(validators=validate_generic)
def put_watched_page(request):
    """
        Edit watched page
        Can change the link text and name, but not repo or mtime/atime
    """
    pass

@watch_page.post(validators=validate_generic)
def post_watched_page(request):
    """
        Add a new watched page
        Need check to make sure user owns repo
    """
    tr = TrackedLink.from_dict(request.validated)
    DBSession.add(tr)
    DBSession.commit()
    return tr.to_dict()
