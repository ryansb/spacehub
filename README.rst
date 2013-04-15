Pyramid on Red Hat's OpenShift Express
======================================

This quickstart helps you get up and running with a Pyramid installation on
OpenShift. It automatically handles creating a Python virtualenv, populating a
MySQL database, and deploying your application to the cloud.

* Create an account at http://openshift.redhat.com/

Features
--------

* Completely free, thanks to Red Hat's OpenShift Express
* MySQL database automatically setup for your application
* Dynamic database configuration at runtime. No passwords stored in your configs.
* Your application's test suite is run after each push
* Automatic deployment upon git push
* No need to think about servers, let alone apache/mod_wsgi configuration

The fastest method
------------------

You can easily deploy a pre-configured Pyramid + MySQL application to the
OpenShift cloud with a single command, using the `openshift-quickstarter` tool:
http://github.com/lmacken/openshift-quickstarter

::

    ./openshift-quickstarter EMAIL DOMAIN APPNAME cornice

That's all it takes. You can now view your application at:

::

    http://APPNAME-DOMAIN.rhcloud.com

Right now, all it'll say is '{"hello": "world"}'

The manual method
-----------------

If you don't want to use the `openshift-quickstarter`, you can easily create a new OpenShift WSGI application and merge this quickstart into it manually:

::

    rhc app create -a corniceapp -t python-2.7 -l your@email.com
    rhc cartridge add -a corniceapp -c mysql-5.1 -l your@email.com
    cd corniceapp
    git remote add upstream -m master git://github.com/ryansb/cornice-openshift-quickstart.git
    git pull -s recursive -X theirs upstream master
    git push

Monitoring your logs
--------------------

::

    rhc tail corniceapp
