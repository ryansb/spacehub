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
from corniceapp.models import User, DBSession
from corniceapp.validators import valid_user, valid_body
from corniceapp.errors import _401
import hashlib


aliens = Service(name='aliens', path='/aliens', description="ALIENS")

@aliens.get()
def aliens_get(request):
    return {"ALIENS": ["http://supb.ro/ALIENS" for r in xrange(1000)]}


users = Service(name='users', path='/users', description="User management api")


@users.get()
def get_users(request):
    """Get all users, privs: admin"""
    users = DBSession.query(User).all()
    scrubbed_users = []
    for user in users:
        scrubbed = {
            "username": user.name,
            "id": user.id,
            "repos": [r.to_dict() for r in user.repos],
            "apikeys": [a.apikey for a in user.apikeys],
        }
        scrubbed_users.append(scrubbed)
    return {"users": scrubbed_users}



@users.post(validators=valid_body(("username", "password", "email")))
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
    if DBSession.query(User).filter(User.name==new_user.name).count() > 0:
        raise _401()
    DBSession.add(new_user)
    DBSession.commit()
    return {"success": True}


@users.put(validators=[valid_body(('username', 'changes')), valid_user])
def edit_user(request):
    """
        Edit an existing user
        privs: logged in, or admin
        {"username": "target", "changes": {"username": "change", "password": "changed", "email": "changed"}}
    """
    cur_user = request.validated['ValidUser']
    target_username = request.validated['username']
    target_users = DBSession.query(User).filter(User.name==target_username)
    if target_users.count() > 1:
        target_user = target_users.first()
        if target_user.name == cur_user.name or cur_user.admin:
            changes = request.validated['changes']
            if "username" in changes:
                if not DBSession.query(User).filter(User.name==changes['username']).count() > 1:
                    target_user.name = changes['username']
            if "password" in changes:
                target_user.password = hashlib.sha512(changes['password']).hexdigest()
            if "email" in changes:
                if not DBSession.query(User).filter(User.email==changes['email']).count() > 1:
                    target_user.email = changes['email']
            DBSession.add(target_user)
            DBSession.commit()
            return {"success": True}
    raise _401()



@users.delete(validators=[valid_body(('username')), valid_user])
def delete_user(request):
    """
        Delete a user
        privs: admin, or self
    """
    cur_user = request.validated['ValidUser']
    target_query = DBSession.query(User).filter(User.name==request.validated['username'])
    if target_query.count() > 0:
        target = target_query.first()
        if target.name == cur_user.name or cur_user.admin:
            DBSession.delete(target)
            DBSession.commit()
            return {"success": True}
    raise _401()
