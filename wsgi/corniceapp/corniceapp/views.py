""" Cornice services.
"""
from cornice import Service
from corniceapp.models import User, Repo, DBSession


hello = Service(name='hello', path='/', description="Simplest app")


users = Service(name='users', path='/users', description="User management api")


@users.get()
def get_users(request):
    """Get all users"""
    users = User.all()
    scrubbed_users = []
    for user in users:
        scrubbed = {
            "username": user.username,
            "repos": user.repos
        }
        scrubbed_users.append(scrubbed)
    return scrubbed_users



@users.post()
def create_user(request):
    """
        Create a new User
        This is expected a username, password, and email
    """
    new_user = User(
        username=request.validated['username'],
        password=request.validated['password'],
        email=request.validated['email']
    )
    DBSession.add(new_user)

@users.put()
def edit_user(request):
    """ Edit an existing user """
    pass


@users.delete()
def delete_user(request):
    """Delete a user"""
    pass


apikeys = Service(name='apikeys', path='/apikeys', description="Manage API keys")


@apikeys.post()
def create_key(request):
    """Create a new api key for a user"""
    pass


@apikeys.delete()
def delete_key(request):
    """Delete an api key"""
    pass


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
