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

from corniceapp.views.sessions import *
from corniceapp.views.users import *
from corniceapp.views.repos import *
