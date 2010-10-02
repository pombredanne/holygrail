#!/usr/bin/python
# -*- coding:Utf-8 -*-

from distutils.core import setup, find_packages

setup(name='HolyGrail',
      version='0.1 Galahad',
      description='High level lib to manage the holy quests of your life (in other words GTD next actions)',
      author='Laurent Peuch',
      author_email='cortex@worlddomination.be',
      url='http://blog.worlddomination.be/holygrail',
      packages=find_packages(),
      install_requires=['sqlobject',
                        'ConfigParser'
                       ]
     )

# vim:set shiftwidth=4 tabstop=4 expandtab:
