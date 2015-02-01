#!/usr/bin/env python

from distutils.core import setup
from src import _version as version
import glob

data_files_icons = glob.glob('gui/*.png')
data_files_gtk = glob.glob('gui/*.glade')

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
                        ('/usr/share/linux-gravatar/', data_files_gtk),
                        ('/usr/share/linux-gravatar/', data_files_icons),
                        ('/usr/share/applications/', ['gui/linux-gravatar.desktop'])],
      packages=['linux-gravatar'],
      )
