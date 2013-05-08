import os
import os.path
import sh
import logging
import sys
from sh import cp
from datetime import datetime
from spacehub.models import DBSession, Repo, TrackedLink
from sqlalchemy import engine_from_config
from paste.deploy import appconfig


logger = logging.getLogger("spacehub.cron")
db_name = "spacehub"

def _getpathsec(config_uri, name):
    if '#' in config_uri:
        path, section = config_uri.split('#', 1)
    else:
        path, section = config_uri, 'main'
    if name:
        section = name
    return path, section


def sync_tarballs(DBSession):
    logger.info(("Syncing Tarball links"))

    links = DBSession.query(TrackedLink).all()
    for link in links:
        repo = DBSession.query(Repo).filter(Repo.id==link.repo_id).first()
        try:
            repo.clone()
        except Exception as e:
            logger.info("Exception found: " + str(e.args))
            return
        extracted_dir = link.retrieve()
        cp('-R', sh.glob('{0}/*'.format(extracted_dir)), repo.dirname)
        repo.commit_a("Automated tarball sync: {0}".format(link.modified.strftime("%D %H:%M")))
        repo.push()
        repo.last_updated = datetime.now()
        DBSession.add(repo)
        DBSession.commit()
        logger.info("Synced {0} -> {1}".format(link.name, repo.name))


def sync_svn(DBSession):
    print("Syncing svn repos")
    repos = DBSession.query(Repo).filter(Repo.source_type=='svn')
    for repo in repos:
        try:
            repo.clone()
        except:
            pass
        svnurl = repo.source_url
        pass


def usage():
    print('usage: spacehub-cron <config_uri>')
    sys.exit(1)


def update_repos():
    if len(sys.argv) != 2:
        usage()
    config_uri = sys.argv[1]
    path, section = _getpathsec(config_uri, "pyramid")
    config_name = 'config:{0}'.format(path)
    here = os.getcwd()
    settings = appconfig(config_name, name=section, relative_to=here)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    sync_tarballs(DBSession)



