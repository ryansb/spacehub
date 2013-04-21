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


repo = Service(name='repo', path='/repo', description="Service to deal with "
              "the addition/deletion of repositories")
repo_param = Service(name='repo', path='/repo/{rid}', description="Service to "
                     "deal with the addition/deletion of repositories")

@repo.get()
def get_repos(request):
    return {"repos": [r.to_dict() for r in DBSession.query(Repo).all()]}


@repo_param.put()
def put_repo(request):
    """
        To edit an existing repository
    """
    print request.matchdict['rid']
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
