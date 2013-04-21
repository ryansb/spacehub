import sys
from corniceapp.models import DBSession, Secret, Repo
from sqlalchemy import engine_from_config
from paste.deploy import appconfig

def _getpathsec(config_uri, name):
    if '#' in config_uri:
        path, section = config_uri.split('#',1)
    else:
        path, section = config_uri, 'main'
    if name:
        section = name
    return path, section

def update_repos():
    if len(sys.argv) != 2:
        exit()
    config_uri = argv[1]
    path, section = _getpathsec(config_uri, "pyramid")
    config_name = 'config:%s' % path
    here_dir = os.getcwd()
    settings = appconfig(config_name, name=section, relative_to=here_dir)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    repos = DBSession.query(Repo).all()
    for repo in repos:
        pass

