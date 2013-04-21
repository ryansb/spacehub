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


users = Service(name='users', path='/users', description="User management api")


@users.get()
def get_users(request):
    """Get all users, privs: admin"""
    users = DBSession.query(User).all()
    scrubbed_users = []
    for user in users:
        scrubbed = {
            "username": user.name,
            "repos": [r.to_dict() for r in user.repos],
        }
        scrubbed_users.append(scrubbed)
    return {"users": scrubbed_users}



@users.post(validators=validate_generic)
def create_user(request):
    """
        Create a new User
        This is expected a username, password, and email
        privs: None
    """
    new_user = User(
        name=request.validated['username'],
        password=hashlib.sha512(request.validated['password']).hexdigest(),
        email=request.validated['email']
    )
    DBSession.add(new_user)
    return {"success": True}

@users.put(validators=validate_generic)
def edit_user(request):
    """
        Edit an existing user
        privs: logged in
    """
    pass


@users.delete(validators=validate_generic)
def delete_user(request):
    """
        Delete a user
        privs: admin, or self
    """
    pass

