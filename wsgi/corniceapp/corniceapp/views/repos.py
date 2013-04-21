""" Cornice services.
"""
from cornice import Service
from corniceapp.models import Repo, DBSession


repo = Service(name='repo', path='/repo', description="Service to deal with "
              "the addition/deletion of repositories")
repo_param = Service(name='repo', path='/repo/{rid}', description="Service to "
                     "deal with the addition/deletion of repositories")
repo_act = Service(name='repo', path='/repo/act/{rid}', description="Service to "
                     "deal with the addition/deletion of repositories")



@repo_act.put()
def commit_repo(request):
    """
        commit whatever changes have been made
    """
    print request.matchdict['rid']
    print request.matchdict['rid']
    r = DBSession.query(Repo).filter(Repo.id==1).first()
    r.commit_a(request.json.get("message"))
    return "yupyup"

@repo_act.get()
def clone_repo(request):
    """
        clone a repo fresh
    """
    print request.matchdict['rid']
    r = DBSession.query(Repo).filter(Repo.id==1).first()
    r.clone()
    return "lololol"


@repo.get()
def get_repos(request):
    return {"repos": [r.to_dict() for r in DBSession.query(Repo).all()]}

@repo.post()
def post_repo(request):
    """
        To create a new repository
    """
    r = Repo.from_dict(request.json)
    DBSession.add(r)
    DBSession.commit()
    return r.to_dict()

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
