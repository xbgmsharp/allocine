#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
A module to use Allocine API V3 in Python
Repository: https://github.com/lovasoa/allocine
Base on work from: https://github.com/gromez/allocine-api
License: LGPLv2 http://www.gnu.org/licenses/lgpl.html

Sample code:

    from allocine import allocine
    api = allocine()
    movie = api.movie(27405)
    search = api.search("Oblivion")

"""
from allocine.api import allocine
