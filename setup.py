#!/usr/bin/env python

from distutils.core import setup

setup(name='linux-gravatar',
      version='0.1.0',
      description='Set your Linux profile picture using gravatar',
      author='jrosco',
      author_email='joel_c@zoho.com',
      url='http://jrosco.github.io/linux-gravatar/',
      license='GPL',
      package_dir={'linux-gravatar': 'src'},
      data_files=[('/usr/share/icons', ['src/media/gravatar.png'])],
      packages=['linux-gravatar'],
      )
