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

import json
from corniceapp.models import DBSession, User, APIKey
from pyramid.security import authenticated_userid


def valid_user(request):

    email = authenticated_userid(request)
    if email:
        try:
            loggedin_user = DBSession.query(User).filter(User.email==email).one()
        except:
            loggedin_user = None
        if loggedin_user:
            request.validated['ValidUser'] = loggedin_user
            request.validated['isAdmin'] = loggedin_user.admin


def validate_generic(request):
    """
    Generic validator that doesn't really do anything
    For testing/rapid dev stuff
    """
    data = json.loads(request.body)
    request.validated.update(data)
    valid_user(request)


