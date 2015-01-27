Python LeTOH-app experiment

This project uses a weird buildout based build approach to make it possible
to easily include and package 3rd party Python packages when required.


Building for development
------------------------

.. code:: bash

   $ python3 bootstrap
   $ qml/buildout
   $ sailfish-qml harbour-myletoh


Packaging a release from a tag
------------------------------

.. code:: bash

   $ cd ~/rpmbuild/SOURCES
   $ curl -L -o harbour-pyletoh-0.1.0.tar.gz https://github.com/datakurre/harbour-pyletoh/archive/0.1.0.tar.gz
   $ tar xzvf harbour-pyletoh-0.1.0.tar.gz
   $ rpmbuild -bb harbour-pyletoh-0.1.0/rpm/harbour-pyletoh.spec

Release is build for arch armv7hl, because this may later contain
compiled arch dependent Python C extensions.
