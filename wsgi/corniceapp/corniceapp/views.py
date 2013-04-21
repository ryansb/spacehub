""" Cornice services.
"""
from cornice import Service
from corniceapp.models import User, Repo, DBSession
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
)
from webob import Response
import hashlib
import json


hello = Service(name='hello', path='/', description="Simplest app")


login = Service(name='users', path='/users/login', description='User login endpoints')


@login.post()
def login_user(request):
    """
        login a user
        privs: none
    """
    password = hashlib.sha512(request.validated['password']).hexdigest()
    username = request.validated['username']
    user = DBSession.query(User).filter(name=username).one()
    if user.password == password:
        headers = remember(request, user.email)
        resp = Response(json.dumps({"success": True}))
        resp.headerlist.extend(headers)
        return resp
    else:
        return {"success": False}


@login.delete()
def logout_user(request):
    """
        logout a user
        privs: logged in
    """
    headers = forget(request)
    pass


users = Service(name='users', path='/users', description="User management api")


@users.get()
def get_users(request):
    """Get all users, privs: admin"""
    users = DBSession.query(User).all()
    scrubbed_users = []
    for user in users:
        scrubbed = {
            "username": user.name,
            "repos": user.repos
        }
        scrubbed_users.append(scrubbed)
    return scrubbed_users



@users.post()
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

@users.put()
def edit_user(request):
    """
        Edit an existing user
        privs: logged in
    """
    pass


@users.delete()
def delete_user(request):
    """
        Delete a user
        privs: admin, or self
    """
    pass


apikeys = Service(name='apikeys', path='/apikeys', description="Manage API keys")


@apikeys.post()
def create_key(request):
    """
        Create a new api key for a user
        privs: logged in, admin
    """
    pass


@apikeys.delete()
def delete_key(request):
    """
        Delete an api key
        privs: logged in, admin
    """
    pass


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}


repo = Service(name='repo', path='/repo', description="Service to deal with "
              "the addition/deletion of repositories")

@repo.get()
def get_repos(request):
    return {"repos": [r.to_dict() for r in DBSession.query(Repo).all()]}


@repo.put()
def put_repo(request):
    """
        To edit an existing repository
    """
    pass


@repo.post()
def post_repo(request):
    """
        To create a new repository
    """
    pass
