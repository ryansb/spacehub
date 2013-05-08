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

from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPMovedPermanently
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from sqlalchemy import engine_from_config
from spacehub.models import initialize_sql


db_name = "spacehub"


def main(global_config, **settings):
    authn_policy = AuthTktAuthenticationPolicy(
        secret='changemeplease')
    authz_policy = ACLAuthorizationPolicy()

    session_factory = UnencryptedCookieSessionFactoryConfig(
        settings['session.secret'])

    config = Configurator(settings=settings, session_factory=session_factory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_static_view('/app', 'static', cache_max_age=3600)
    config.add_view(lambda r: HTTPMovedPermanently(location='/app/index.html'),
                    context='pyramid.httpexceptions.HTTPNotFound')
    config.include("cornice")
    config.scan("spacehub.views")
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

    return config.make_wsgi_app()
