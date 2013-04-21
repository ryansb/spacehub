from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Unicode, Text, DateTime, ForeignKey, Column, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from datetime import datetime
from shlex import split
import subprocess
import git
import os.path


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
        print "Setting push job"
        subprocess.check_call(split('cd {0} && git push --all origin').format(self.dirname))
        return True

    def commit_a(self, message):
        if not os.path.exists(self.dirname):
            self.clone()
        r = git.Repo(self.dirname)
        r.git.add(self.dirname)
        r.git.commit('-am "%s"' % message)
        return True



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
