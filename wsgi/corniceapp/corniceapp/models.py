"""
   SpaceHub
   Copyright (C) 2013 Ryan Brown <sb@ryansb.com>, Sam Lucidi <mansam@csh.rit.edu>,
   Ross Delinger <rossdylan@csh.rit.edu>, Greg Jurman <jurman.greg@gmail.com>

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            email=self.email,
            admin=self.admin,
            created_at=self.created_at.strftime("%D %H:%M"),
            repos=[r.to_dict() for r in self.repos],
            apikey=[a.to_dict() for a in self.apikeys])


class APIKey(_Base):
    __tablename__ = "apikeys"

    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime())
    apikey = Column(Unicode(255))
    owner_id = Column(Integer, ForeignKey('users.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            create_at=self.create_at,
            apikey=self.apikey,
            owner_id=self.owner_id)


class Secret(_Base):
    __tablename__ = "secrets"
    id = Column(Integer, primary_key=True)
    oauth = Column(Text())
    private_key = Column(Text())
    public_key = Column(Text())
    comment = Column(Text())


class Repo(_Base):
    __tablename__ = "repos"
    __mapper_args__ = dict(order_by="created_at desc")

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(Unicode(255))
    created_at = Column(DateTime())
    last_updated = Column(DateTime())
    source_url = Column(Text())
    github_uname = Column(Text())
    github_repo = Column(Text())
    clone_url = Column(Text())
    dirname = Column(Text())
    source_type = Column(Text())

    @property
    def github_url(self):
        return "git@github.com:%s/%s.git" % (self.github_uname, self.github_repo)

    def to_dict(self):
        return dict(
            id=self.id,
            owner_id=self.owner_id,
            name=self.name,
            created_at=self.created_at.strftime("%D %H:%M"),
            last_updated=self.last_updated.strftime("%D %H:%M"),
            source_url=self.source_url,
            github_uname=self.github_uname,
            github_repo=self.github_repo,
            github_url=self.github_url,
            clone_url=self.clone_url,
            dirname=self.dirname,
            source_type=self.source_type
        )

    @classmethod
    def from_dict(cls, new):
        r = Repo()
        r.owner_id = new.get('owner_id')
        r.name = new.get('name')
        r.created_at = datetime.now()
        r.last_updated = datetime.now()
        r.source_url = new.get('source_url')
        r.github_uname = new.get('github_uname')
        r.github_repo = new.get('github_repo')
        r.clone_url = new.get('clone_url')
        r.dirname = new.get('dirname')
        r.source_type = new.get('source_type')
        return r

    def updict(self, new):
        self.name = new.get('name', self.name)
        self.last_updated = datetime.now()
        self.source_url = new.get('source_url', self.source_url)
        self.github_uname = new.get('github_uname', self.github_uname)
        self.github_repo = new.get('github_repo', self.github_repo)
        self.clone_url = new.get('clone_url', self.clone_url)
        self.source_type = new.get('source_type', self.source_type)
        self.dirname = new.get('dirname', self.dirname)
        return True

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
        r.git.add(os.path.join(self.dirname, "*"))
        try:
            r.git.commit('-m "%s"' % message)
        except:
            return False
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
