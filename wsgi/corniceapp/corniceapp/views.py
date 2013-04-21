""" Cornice services.
"""
from cornice import Service
from corniceapp.models import User, Repo, DBSession
from corniceapp.models import User, Repo, DBSession, TrackedLink, ScrapeJob
from corniceapp.validators import validate_generic
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
)
from webob import Response
import hashlib
import json


login = Service(name='users', path='/users/login', description='User login endpoints')


@login.post(validators=validate_generic)
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
    resp = Response(json.dumps({"success": True}))
    resp.headerlist.extend(headers)
    return resp


users = Service(name='users', path='/users', description="User management api")


@users.get(validators=validate_generic)
def get_users(request):
    """Get all users, privs: admin"""
    users = DBSession.query(User).all()
    scrubbed_users = []
    for user in users:
        scrubbed = {
            "username": user.name,
            "repos": user.repos.to_dict()
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


apikeys = Service(name='apikeys', path='/apikeys', description="Manage API keys")


@apikeys.post(validators=validate_generic)
def create_key(request):
    """
        Create a new api key for a user
        privs: logged in, admin
    """
    pass


@apikeys.delete(validators=validate_generic)
def delete_key(request):
    """
        Delete an api key
        privs: logged in, admin
    """
    pass


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
    r = Repo.from_dict(request.json)
    DBSession.add(r)
    DBSession.commit()
    return r.to_dict()



watch_page = Service(name="watch_page", path="/watch_page",
        description="Service to deal with watching page links for changed files")

@watch_page.get()
def get_watched_page(request):
    return TrackedLinks.all()

@watch_page.put()
def put_watched_page(request):
    """
        Edit watched page
    """
    pass

@watch_page.post()
def post_watched_page(request):
    """
        Add a new watched page
    """
    pass



watch_runner = Service(name="watch_runner", path="/watch_runner",
        description="Service to run the watcher for watched pages")

@watch_runner.post()
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

@watch_runner.get()
def get_watch_runner(request):
    """
        When GET'd to this, will get info on the running jorb
    """
    pass
