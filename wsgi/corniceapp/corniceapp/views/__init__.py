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

from corniceapp.views.sessions import *
from corniceapp.views.users import *
from corniceapp.views.repos import *
