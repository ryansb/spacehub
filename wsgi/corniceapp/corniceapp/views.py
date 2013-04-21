""" Cornice services.
"""
from cornice import Service
from corniceapp.models import User, Repo


hello = Service(name='hello', path='/', description="Simplest app")


@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}


repo = Service(name='repo', path='/repo', description="Service to deal with "
              "the addition/deletion of repositories")

@repo.get()
def get_repos(request):
    return Repo.all()


@repo.put()
def put_repo(request):
    """
        To edit an existing repository
    """
    pass


@repo.post()
def post_repo(request):
    """
        To create a new repository
    """
    pass
