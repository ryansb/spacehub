""" Cornice services.
"""
from cornice import Service


hello = Service(name='hello', path='/', description="Simplest app")

users = Service(name='users', path='/users', description="User management api")

@users.get()
def get_user(request):
    pass

@users.post()
def create_user(request):
    pass

@users.delete()
def delete_user(request):
    pass

@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}
