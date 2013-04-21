""" Cornice services.
"""
from cornice import Service
from corniceapp.models import User, DBSession, APIKey
from corniceapp.validators import validate_generic
from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
)
from webob import Response
import hashlib
import json
import uuid


login = Service(name='users', path='/users/login', description='User login endpoints')


def get_logged_in_user(request):
    """
        Return the user authenticated in this request
    """
    email = authenticated_userid(request)
    return DBSession.query(User).filter(User.email==email).one()


def gen_apikey():
    """
        Generate a unique api key
    """
    for _ in range(10):
        newkey = str(uuid.uuid5()).replace('-', '')
        if DBSession.query(APIKey).filter(APIKey.apikey==newkey).count() == 0:
            return newkey
    raise Exception("can't make a unique key... wat")


@login.post(validators=validate_generic)
def login_user(request):
    """
        login a user
        privs: none
        {"username": "name", "password": "pass"}
    """
    password = hashlib.sha512(request.validated['password']).hexdigest()
    username = request.validated['username']
    user = DBSession.query(User).filter(User.name==username).one()
    if user and user.password == password:
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



apikeys = Service(name='apikeys', path='/apikeys', description="Manage API keys")


@apikeys.post(validators=validate_generic)
def create_key(request):
    """
        Create a new api key for a user
        privs: logged in, admin
        {"username": "dat-user"}
    """
    cur_user = request.validated['ValidUser']
    if cur_user:
        target_user = DBSession.query(User).filter(
            User.name==request.validated['username']).one()
        if target_user.name == cur_user or cur_user.admin:
            key = gen_apikey()
            newAPIKey = APIKey(apikey=key,ownerid=target_user.id)
            DBSession.add(newAPIKey)
            return {"success": True}
    return {"success": False}


@apikeys.delete(validators=validate_generic)
def delete_key(request):
    """
        Delete an api key
        privs: logged in, admin
        {"username": "user", "key": "dat-key"}
    """
    cur_user = request.validated['ValidUser']
    if cur_user:
        target_user = DBSession.query(User).filter(
            User.name==request.validated['username']).one()
        if target_user == cur_user or cur_user.admin:
            key = DBSession.query(APIKey).filter(
                APIKey.apikey==request.validated['key']).one()
            DBSession.delete(key)
            return {"success": True}
    return {"success": False}

