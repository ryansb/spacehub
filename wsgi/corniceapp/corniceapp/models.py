from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Unicode, Text, DateTime, ForeignKey, Column
from sqlalchemy.orm import scoped_session, sessionmaker, relationship


_Base = declarative_base()
DBSession = scoped_session(sessionmaker())


class User(_Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))
    email = Column(Unicode(255))
    created_at = Column(DateTime())
    password = Column(Unicode(255))
    repos = relationship("Repo")
    apikeys = relationship("APIKey")


class APIKey():
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
    path = Column(Text())

    def to_dict(self):
        return dict(
            owner_id=self.owner_id,
            name=self.name,
            created_at=self.created_at,
            last_updated=self.last_updated,
            source_url=self.source_url,
            github_url=self.github_url,
            path=self.path
        )


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    _Base.metadata.bind = engine
    _Base.metadata.drop_all()
    _Base.metadata.create_all(engine, checkfirst=False)
