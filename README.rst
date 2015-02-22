Python LeTOH controller experiment

This project uses a weird buildout based build approach to make it possible
to easily include and package 3rd party Python packages when required.


In-device development
---------------------

It's most convenient to develop pyLeTOH with a real Jolla-device with the
LeTOH other half.

1. Install the packaged app_ to get everything configured for free.

2. Clone this repository on top of the installed app into
   ``/usr/share/harbour-pyletoh``.

3. Bootstrap and run the buildout to get startup scripts.

   .. code:: bash

      $ python3 bootstrap
      $ qml/buildout
      $ sailfish-qml harbour-pyletoh

4. Develop.

.. _app: https://openrepos.net/content/datakurre/pyletoh


Hacking with the library
------------------------

pyLeTOH can also be used as a pure pythoh library for custom hacking with
the LeTOH.

1. Create a python virtualenv with system packages enabled and this
   the library installed

   .. code:: bash

      $ pyvenv MyLeTOH
      $ source MyLeTOH/bin/activate
      $ pip install git+https://github.com/datakurre/harbour-pyletoh#egg=letoh
      $ sed -i -e 's/false/true/g' MyLeTOH/pyvenv.cfg

2. Use this library from your Python code

   .. code:: python

      # Import
      from letoh import LeTOH

      # Instantiate
      myletoh = LeTOH()

      # Set all leds or the same color
      myletoh('#FF0000')

      # Set named leds for a particular color
      myletoh({'topleft': '#0000FF'})

      # Shutdown all the leds
      myletoh('#000000')


Releases
--------

`Built at Nemo OBS`__

__ https://build.merproject.org/package/show/home:datakurre/harbour-pyletoh

`Distributed by Open Repos`__

__ https://openrepos.net/content/datakurre/harbour-pyletoh
