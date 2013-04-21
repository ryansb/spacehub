import json
from corniceapp.models import DBSession, User, APIKey
from pyramid.security import authenticated_userid


def validate_generic(request):
    """
    Generic validator that doesn't really do anything
    For testing/rapid dev stuff
    """
    data = json.loads(request.body)
    request.validated.update(data)

    email = authenticated_userid(request)
    loggedin_user = DBSession.query(User).filter(email=email).one()
    if loggedin_user:
        request.validated['ValidUser'] = loggedin_user
        request.validated['isAdmin'] = loggedin_user.admin

