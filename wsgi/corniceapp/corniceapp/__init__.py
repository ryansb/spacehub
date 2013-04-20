"""Main entry point
"""
from pyramid.config import Configurator

import os


db_name = "spacehub"

db_url = "sqlite:////tmp/test.db"

if os.environ.get("OPENSHIFT_MYSQL_DB_URL", None):
    db_url = os.environ.get("OPENSHIFT_MYSQL_DB_URL") + db_name



def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("corniceapp.views")
    return config.make_wsgi_app()
