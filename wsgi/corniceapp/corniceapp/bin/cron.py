import sys
import os
import os.path
from sh import cp
from corniceapp.models import DBSession, Repo, TrackedLink
from sqlalchemy import create_engine


db_name = "spacehub"

db_url = "sqlite:////tmp/test.db"


if os.environ.get("OPENSHIFT_MYSQL_DB_URL", None):
    db_url = os.environ.get("OPENSHIFT_MYSQL_DB_URL") + db_name


def sync_tarballs():
    if len(sys.argv) != 2:
        exit()

    engine = create_engine(db_url)
    DBSession.configure(bind=engine)

    links = DBSession.query(TrackedLink).all()
    for link in links:
        repo = DBSession.query(Repo).filter(Repo.id==link.repo_id).first()
        try:
            repo.clone()
        except:
            pass
        extracted_dir = link.retrieve()
        cp("-r {0} {1}".format(os.path.join(extracted_dir, "*"), repo.dirname))
        repo.commit_a("Automated tarball sync: {0}".format(link.modified.strftime("%D %H:%M")))
        print("Synced {0} -> {1}".format(link.name, repo.name))

def update_repos():
    print("Syncing Tarball links")
    sync_tarballs()



