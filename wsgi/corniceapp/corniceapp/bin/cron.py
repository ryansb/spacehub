import os
import os.path
import sh
from datetime import datetime
from sh import cp
from corniceapp.models import DBSession, Repo, TrackedLink
from sqlalchemy import create_engine
import logging


logger = logging.getLogger("spacehub.cron")
db_name = "space"

db_url = "sqlite:////tmp/test.db"


if os.environ.get("OPENSHIFT_MYSQL_DB_URL", None):
    db_url = os.environ.get("OPENSHIFT_MYSQL_DB_URL") + db_name


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


def update_repos():
    engine = create_engine(db_url)
    DBSession.configure(bind=engine)
    sync_tarballs(DBSession)



