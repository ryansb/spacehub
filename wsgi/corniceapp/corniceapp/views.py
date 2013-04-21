""" Cornice services.
"""
from cornice import Service


hello = Service(name='hello', path='/', description="Simplest app")

users = Service(name='users', path='/users/{username}', description="User management api")
apikeys = Service(name='apikeys', path='/apikeys', description="Manage API keys")


@users.get()
def get_user(request):
    """Get info on user"""
    pass

@users.post()
def create_user(request):
    """Create a new User"""
    pass

@users.delete()
def delete_user(request):
    """Delete a user"""
    pass


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
