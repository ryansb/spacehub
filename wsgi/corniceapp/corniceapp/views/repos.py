""" Cornice services.
"""
from cornice import Service
from corniceapp.models import Repo, DBSession


repo = Service(name='repo', path='/repo', description="Service to deal with "
              "the addition/deletion of repositories")
repo_param = Service(name='repo', path='/repo/{rid}', description="Service to "
                     "deal with the addition/deletion of repositories")



@repo_param.put()
def put_repo(request):
    """
        To edit an existing repository
    """
    print request.matchdict['rid']
    print request.matchdict['rid']
    r = DBSession.query(Repo).filter(Repo.id==1).first()
    r.commit_a(request.json.get("message"))
    return "yupyup"

@repo_param.get()
def get_repo(request):
    """
        View an exisiting repository
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
