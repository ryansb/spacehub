"""
   SpaceHub
   Copyright (C) 2013 Ryan Brown <sb@ryansb.com>, Sam Lucidi <mansam@csh.rit.edu>,
   Ross Delinger <rossdylan@csh.rit.edu>, Greg Jurman <jurman.greg@gmail.com>

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from cornice import Service
from corniceapp.models import User, DBSession, APIKey
from corniceapp.validators import validate_generic
from corniceapp.errors import _401
from pyramid.security import (
    remember,
    forget,
)
from webob import Response
import hashlib
import json
import uuid


login = Service(name='users', path='/users/login', description='User login endpoints')


def gen_apikey():
    """
        Generate a unique api key
    """
    for _ in range(10):
        newkey = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'spacehub.org')).replace('-', '')
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
    try:
        user = DBSession.query(User).filter(User.name==username).one()
    except:
        raise _401()
    if user and user.password == password:
        headers = remember(request, user.email)
        resp = Response(json.dumps({"success": True}))
        resp.headerlist.extend(headers)
        return resp
    else:
        raise _401()


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
    print("cur_user: " + str(cur_user))
    if cur_user:
        try:
            target_user = DBSession.query(User).filter(
                User.name==request.validated['username']).one()
            print("target_user: " + str(target_user))
        except:
            target_user = None

        if target_user and (target_user.name == cur_user or cur_user.admin):
            key = gen_apikey()
            newAPIKey = APIKey(apikey=key,owner_id=target_user.id)
            DBSession.add(newAPIKey)
            DBSession.commit()
            return {"success": True}
    raise _401()

@apikeys.delete(validators=validate_generic)
def delete_key(request):
    """
        Delete an api key
        privs: logged in, admin
        {"username": "user", "key": "dat-key"}
    """
    cur_user = request.validated['ValidUser']
    if cur_user:
        try:
            target_user = DBSession.query(User).filter(
                User.name==request.validated['username']).one()
        except:
            target_user = None
        if target_user and (target_user == cur_user or cur_user.admin):
            try:
                key = DBSession.query(APIKey).filter(
                    APIKey.apikey==request.validated['key']).one()
            except:
                key = None
            if key:
                DBSession.delete(key)
                DBSession.commit()
                return {"success": True}
    raise _401()
