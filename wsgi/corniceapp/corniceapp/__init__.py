"""Main entry point
"""
from pyramid.config import Configurator

import os
from sqlalchemy import create_engine
from corniceapp.models import initialize_sql


db_name = "missioncontrol"

db_url = "sqlite:////tmp/test.db"

if os.environ.get("OPENSHIFT_MYSQL_DB_URL", None):
    db_url = os.environ.get("OPENSHIFT_MYSQL_DB_URL") + db_name


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_static_view('/', 'static', cache_max_age=3600)
    config.include("cornice")
    config.scan("corniceapp.views")
    engine = create_engine(db_url)
    initialize_sql(engine)
    return config.make_wsgi_app()
