#!/usr/bin/env python

from distutils.core import setup
from linuxgravatar import _version as version
import glob

data_files_icons = glob.glob('data/gui/*.png')
data_files_gtk = glob.glob('data/gui/*.glade')

setup(name=version.__name__,

      version=version.__version__,

      description=version.__description__,

      author=version.__author__,

      author_email=version.__email__,

      url=version.__website__,

      license=version.__license__,

      packages=['linuxgravatar'],

      scripts=['linux-gravatar'],

      data_files=[('/usr/share/icons', ['data/gui/gravatar.png']),
                  ('/usr/share/linux-gravatar/', data_files_gtk),
                  ('/usr/share/linux-gravatar/', data_files_icons),
                  ('/usr/share/applications/', ['data/gui/linux-gravatar.desktop'])],

      )
