from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Unicode, String, Text, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from datetime import datetime
import subprocess
import git

from uuid import uuid4
from datetime import datetime

_Base = declarative_base()
DBSession = scoped_session(sessionmaker())

repo_path = "/tmp/"


class User(_Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))
    email = Column(Unicode(255))
    admin = Column(Boolean)
    created_at = Column(DateTime())
    password = Column(Unicode(255))
    repos = relationship("Repo")
    apikeys = relationship("APIKey")


class APIKey(_Base):
    __tablename__ = "apikeys"

    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime())
    apikey = Column(Unicode(255))
    owner_id = Column(Integer, ForeignKey('users.id'))


class Repo(_Base):
    __tablename__ = "repos"
    __mapper_args__ = dict(order_by="created_at desc")

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(Unicode(255))
    created_at = Column(DateTime())
    last_updated = Column(DateTime())
    source_url = Column(Text())
    github_url = Column(Text())
    clone_url = Column(Text())
    dirname = Column(Text())

    def to_dict(self):
        return dict(
            owner_id=self.owner_id,
            name=self.name,
            created_at=self.created_at.strftime("%D %H:%M"),
            last_updated=self.last_updated.strftime("%D %H:%M"),
            source_url=self.source_url,
            github_url=self.github_url,
            clone_url=self.clone_url,
            dirname=self.dirname
        )

    @classmethod
    def from_dict(cls, new):
        r = Repo()
        r.owner_id = new.get('owner_id')
        r.name = new.get('name')
        r.created_at = datetime.now()
        r.last_updated = datetime.now()
        r.source_url = new.get('source_url')
        r.github_url = new.get('github_url')
        r.clone_url = new.get('clone_url')
        r.dirname = new.get('dirname')
        return r

    def clone(self):
        print "Setting clone job"
        print ["git", "clone", self.clone_url, self.dirname]
        subprocess.check_call(["git", "clone", self.clone_url, self.dirname])
        return True

    def push(self):
        print "Setting clone job"
        subprocess.check_call('cd %s && git push --all origin'.split(' '))
        return True

    def commit_a(self, message):
        r = git.Repo(self.dirname)
        r.git.add(self.dirname)
        r.git.commit('-am "%s"' % message)
        return True



class TrackedLink(_Base):
    __tablename__ = 'tracked_links'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    last_accessed = Column(DateTime())
    modified = Column(DateTime())
    link_text = Column(Unicode)
    repo_id = Column(Integer, ForeignKey('repos.id'))
    repo = relationship("Repo", backref="track_link")

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            last_access=self.last_accessed,
            last_modified=self.modified,
            link_text=self.link_text,
            repo=self.repo_id
        )

    def from_dict(cls, new):
        t = TrackedLink()
        t.repo_id = new.get('repo_id')
        t.name = new.get('name')
        t.url = new.get('url')
        t.link_text = new.get('link_text')
        return t


class ScrapeJob(_Base):
    __tablename__ = 'watch_jobs'

    id = Column(String(36), default=(lambda: str(uuid4())), primary_key=True)
    starttime = Column(DateTime(), default=(lambda: datetime.now()))
    status = Column(Integer)


def initialize_sql(engine):
    import hashlib
    DBSession.configure(bind=engine)
    _Base.metadata.bind = engine
    _Base.metadata.drop_all()
    _Base.metadata.create_all(engine, checkfirst=False)
    DBSession.add(User(name="admin", password=hashlib.sha512("password").hexdigest(), admin=True, email="admin@spacehub.com"))
    DBSession.add(Repo.from_dict(dict(name="genetic-css", owner_id=1,
                                      source_url="sourceforge.com/lololol",
                                      clone_url="git://github.com/ryansb/genetic-css.git",
                                      github_url="https://github.com/ryansb/genetic-css",
                                      dirname="/tmp/genetic-css")))
    DBSession.commit()
