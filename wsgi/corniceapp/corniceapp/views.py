""" Cornice services.
"""
from cornice import Service
from corniceapp.models import User, Repo, DBSession


users = Service(name='users', path='/users', description="User management api")


@users.get()
def get_users(request):
    """Get all users"""
    users = DBSession.query(User).all()
    scrubbed_users = []
    for user in users:
        scrubbed = {
            "username": user.name,
            "repos": user.repos
        }
        scrubbed_users.append(scrubbed)
    return {"users": scrubbed_users}



@users.post()
def create_user(request):
    """
        Create a new User
        This is expected a username, password, and email
    """
    new_user = User(
        name=request.validated['username'],
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


repo = Service(name='repo', path='/repo', description="Service to deal with "
              "the addition/deletion of repositories")

@repo.get()
def get_repos(request):
    return {"repos": [r.to_dict() for r in DBSession.query(Repo).all()]}


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
    r = Repo.from_dict(request.json)
    DBSession.add(r)
    DBSession.commit()
    return r.to_dict()
