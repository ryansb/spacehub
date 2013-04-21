""" Cornice services.
"""
from cornice import Service
from corniceapp.models import Repo, DBSession
from corniceapp.validators import valid_user
from corniceapp.errors import _401


repo = Service(name='repo', path='/repo', description="Service to deal with "
              "the addition/deletion of repositories")
repo_param = Service(name='repo', path='/repo/{rid}', description="Service to "
                     "deal with the addition/deletion of repositories")
repo_act = Service(name='repo', path='/repo/act/{rid}', description="Service to "
                     "deal with the addition/deletion of repositories")



@repo_act.put(validators=valid_user)
def commit_repo(request):
    """
        commit whatever changes have been made
    """
    cur_user = request.validated['ValidUser']
    if cur_user:
        print request.matchdict['rid']
        print request.matchdict['rid']
        r = DBSession.query(Repo).filter(Repo.id==1).first()
        if r.owner_id == cur_user.id or cur_user.admin:
            r.commit_a(request.json.get("message"))
            return "yupyup"
    raise _401()


@repo_act.get(validators=valid_user)
def clone_repo(request):
    """
        clone a repo fresh
    """
    cur_user = request.validated['ValidUser']
    if cur_user:
        print request.matchdict['rid']
        r = DBSession.query(Repo).filter(Repo.id==1).first()
        if r.owner_id == cur_user.id or cur_user.admin:
            r.clone()
            return "lololol"
    raise _401()


@repo.get(validators=valid_user)
def get_repos(request):
    cur_user = request.validated['ValidUser']
    if cur_user:
        return {"repos": [r.to_dict() for r in DBSession.query(Repo).filter(Repo.owner_id==cur_user.id).all()]}


@repo.post(validators=valid_user)
def post_repo(request):
    """
        To create a new repository
    """
    cur_user = request.validated['ValidUser']
    if cur_user:
        r = Repo.from_dict(request.json)
        r.user_id = cur_user.id
        DBSession.add(r)
        DBSession.commit()
        return r.to_dict()
    raise _401()


@repo_param.get()
def get_param_repo(request):
    return DBSession.query(Repo).filter(Repo.id==request.matchdict['rid']).first().to_dict()


@repo_param.put()
def update_repo(request):
    repo = DBSession.query(Repo).filter(Repo.id==request.matchdict['rid']).first()
    repo.__dict__.update(request.json)
    DBSession.add(repo)
    DBSession.commit()
    return DBSession.query(Repo).filter(Repo.id==request.matchdict['rid']).first().to_dict()
