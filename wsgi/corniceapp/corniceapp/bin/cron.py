import sys
import os
import os.path
from sh import cp
from corniceapp.models import DBSession, Repo, TrackedLink
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


def sync_tarballs():
    if len(sys.argv) != 2:
        exit()
    config_uri = sys.argv[1]
    path, section = _getpathsec(config_uri, "pyramid")
    config_name = 'config:%s' % path
    here_dir = os.getcwd()
    settings = appconfig(config_name, name=section, relative_to=here_dir)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    links = DBSession.query(TrackedLink).all()
    for link in links:
        repo = DBSession.query(Repo).filter(Repo.id==link.repo_id).first()
        try:
            repo.clone()
        except:
            pass
        extracted_dir = link.retreive()
        cp("-r {0} {1}".format(os.path.join(extracted_dir, "*"), repo.dirname))
        repo.commit_a("Automated tarball sync: {0}".format(link.modified.strftime("%D %H:%M")))
        print("Synced {0} -> {1}".format(link.name, repo.name))

def update_repos():
    print("Syncing Tarball links")
    sync_tarballs()



