#!/usr/bin/env python

from distutils.core import setup
from src import _version as version

setup(name=version.__name__,
      version=version.__version__,
      description=version.__description__,
      author=version.__author__,
      author_email=version.__email__,
      url=version.__website__,
      license=version.__license__,
      package_dir={'linux-gravatar': 'src'},
      data_files=[('/usr/share/icons', ['gui/gravatar.png']),
                        ('/usr/bin/', ['bin/linux-gravatar']),
                        ('/usr/share/linux-gravatar/', ['gui/settings_win.glade']),
                        ('/usr/share/linux-gravatar/', ['gui/logo_heading.png']),
                        ('/usr/share/applications/', ['gui/linux-gravatar.desktop'])],
      packages=['linux-gravatar'],
      )
