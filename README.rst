SpaceHub
========

SpaceHub is an open-source scraper for code located on Sourceforge, in SVN, or
just in a tarball somewhere.

Built for the `NASA Space Apps Challenge` http://spaceappschallenge.org to
centralize NASA open source projects.

Features
--------

* Completely free, and runs on OpenShift Express (RedHat++)
* Centralizes projects on Github
* Takes URLs of tarballs and automatically makes commits when they are changed
* Uses Github API to create repos if they do not exist

Get Started
-----------
::

    rhc app create spacehub python-2.7
    rhc cartridge add -a spacehub -c mysql-5.1
    git remote add shift <OPENSHIFT PUSH URL>
    git push shift master -f

That's all it takes. You can now view your application at:

::

    http://APPNAME-DOMAIN.rhcloud.com

And you're off to the races!
