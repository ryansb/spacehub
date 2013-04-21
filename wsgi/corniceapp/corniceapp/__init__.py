"""Main entry point
"""
from pyramid.config import Configurator
from pyramid.authentication import AuthTkAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig

import os
from sqlalchemy import create_engine
from corniceapp.models import initialize_sql


db_name = "missioncontrol"

db_url = "sqlite:////tmp/test.db"

if os.environ.get("OPENSHIFT_MYSQL_DB_URL", None):
    db_url = os.environ.get("OPENSHIFT_MYSQL_DB_URL") + db_name


def main(global_config, **settings):
    authn_policy = AuthTkAuthenticationPolicy(
        secret='changemeplease')
    authz_policy = ACLAuthorizationPolicy()

    session_factory = UnencryptedCookieSessionFactoryConfig(
        settings['session.secret'])

    config = Configurator(settings=settings, session_factory=session_factory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_static_view('/app', 'static', cache_max_age=3600)
    config.include("cornice")
    config.scan("corniceapp.views")
    engine = create_engine(db_url)
    initialize_sql(engine)

    return config.make_wsgi_app()
