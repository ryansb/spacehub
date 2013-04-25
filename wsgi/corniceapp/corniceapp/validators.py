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
from corniceapp.models import DBSession, User
from corniceapp.errors import _401
from pyramid.security import authenticated_userid
import logging


logger= logging.getLogger("spacehub.validation")


def valid_user(request):
    """
        Require that a valid user be logged in to access this path
    """
    email = authenticated_userid(request)
    if email:
        user_query = DBSession.query(User).filter(User.email==email)
        if user_query.count() > 0:
            user = user_query.first()
            request.validated['ValidUser'] = user
            logger.info("User: " + user.name + " " + str(user.id))
        else:
            raise _401()
    else:
        raise _401()


def valid_body(required_keys):
    """
        Create a validation function that makes sure the required keys are
        present
    """
    def valid_body_func(request):
        data = json.loads(request.body)
        if all(map(lambda k: k in data,required_keys)):
            request.validated.update(data)
        else:
            raise _401()
    return valid_body_func


def validate_generic(request):
    """
    Generic validator that doesn't really do anything
    For testing/rapid dev stuff
    """
    data = json.loads(request.body)
    request.validated.update(data)
    valid_user(request)


