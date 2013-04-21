""" Cornice services.
"""
from cornice import Service
from corniceapp.models import User, DBSession
from corniceapp.validators import validate_generic
from corniceapp.errors import _401
import hashlib


aliens = Service(name='aliens', path='/aliens', description="ALIENS")

@aliens.get()
def aliens_get(request):
    return {"ALIENS": ["http://supb.ro/ALIENS" for r in xrange(1000)]}


users = Service(name='users', path='/users', description="User management api")


@users.get()
def get_users(request):
    """Get all users, privs: admin"""
    users = DBSession.query(User).all()
    scrubbed_users = []
    for user in users:
        scrubbed = {
            "username": user.name,
            "id": user.id,
            "repos": [r.to_dict() for r in user.repos],
            "apikeys": [a.apikey for a in user.apikeys],
        }
        scrubbed_users.append(scrubbed)
    return {"users": scrubbed_users}



@users.post(validators=validate_generic)
def create_user(request):
    """
        Create a new User
        This is expected a username, password, and email
        privs: None
    """
    new_user = User(
        name=request.validated['username'],
        password=hashlib.sha512(request.validated['password']).hexdigest(),
        email=request.validated['email']
    )
    if DBSession.query(User).filter(User.name==new_user.name).count() > 0:
        raise _401()
    DBSession.add(new_user)
    return {"success": True}


@users.put(validators=validate_generic)
def edit_user(request):
    """
        Edit an existing user
        privs: logged in, or admin
        {"username": "target", "changes": {"username": "change", "password": "changed", "email": "changed"}}
    """
    cur_user = request.validated['ValidUser']
    if cur_user:
        target_username = request.validated['username']
        target_users = DBSession.query(User).filter(User.name==target_username)
        if target_users.count() > 1:
            target_user = target_users.one()
            if target_user.name == cur_user.name or cur_user.admin:
                changes = request.validated['changes']
                if "username" in changes:
                    if not DBSession.query(User).filter(User.name==changes['username']).count() > 1:
                        target_user.name = changes['username']
                if "password" in changes:
                    target_user.password = hashlib.sha512(changes['password']).hexdigest()
                if "email" in changes:
                    if not DBSession.query(User).filter(User.email==changes['email']).count() > 1:
                        target_user.email = changes['email']
    raise _401()



@users.delete(validators=validate_generic)
def delete_user(request):
    """
        Delete a user
        privs: admin, or self
    """
    cur_user = request.validated['ValidUser']
    if cur_user:
        try:
            target_user = DBSession.query(User).filter(User.name==request.validated['username']).one()
        except:
            target_user = None
        if target_user and (target_user.name == cur_user.name or cur_user.admin):
            DBSession.delete(target_user)
            return {"success": True}
    raise _401()
