#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
A module to use Allocine API V3 in Python
https://github.com/xbgmsharp/allocine
Base on work from https://github.com/gromez/allocine-api

Sample code:

    from allocine import allocine
    api = allocine('100043982026','29d185d98c984a359e6e6f26a0474269')
    movie = api.get(27405)
    search = api.search("Oblivion")
or
    from allocine import allocine
    api = allocine()
    api.configure('100043982026','29d185d98c984a359e6e6f26a0474269')
    movie = api.get(27405)
    search = api.search("Oblivion")

"""
# Debug
#from pprint import pprint
# standard module
from datetime import date
import urllib2, urllib
import hashlib, base64
import simplejson

__version__ = "0.1"
__author__ = "Francois Lacroix"
__license__ = "GPL"
__description__ = "A module to use Allocine API V3 in Python"

class allocine(object):
    """ allocine, used to call Allocine API. """
    def __init__(self, partner_key=None, secret_key=None):
        """Init values"""
        self._api_url = 'http://api.allocine.fr/rest/v3'
        self._partner_key  = partner_key
        self._secret_key = secret_key
        self._user_agent = 'Dalvik/1.6.0 (Linux; U; Android 4.2.2; Nexus 4 Build/JDQ39E)'

    def configure(self, partner_key=None, secret_key=None):
        """Set the keys"""
        self._partner_key = partner_key
        self._secret_key = secret_key

    def _do_request(self, method=None, params=None):
        """Generate and send the request"""
        # build the URL
        query_url = self._api_url+'/'+method;

        # new algo to build the query
        today = date.today()
        sed = today.strftime('%Y%m%d')
        #print sed
        sha1 = hashlib.sha1(self._secret_key+urllib.urlencode(params)+'&sed='+sed).digest()
        #print sha1
        b64 = base64.b64encode(sha1)
        #print b64
        sig = urllib2.quote(b64)
        query_url += '?'+urllib.urlencode(params)+'&sed='+sed+'&sig='+sig
        #print query_url;

        # do the request
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', self._user_agent)]
        
        response = simplejson.load(opener.open(query_url, timeout = 10))
        #pprint(response)
        return response;
    
    def search(self, query):
        """Search for a movie"""
        # build the params
        params = {}
        params['partner'] = self._partner_key
        params['q'] = query
        params['format'] = 'json'
        params['filter'] = 'movie'

        # do the request
        response = self._do_request('search', params);

        return response;

    def get(self, id):
        """Get the movie details by ID"""
        # build the params
        params = {}
        params['partner'] = self._partner_key
        params['code'] = id
        params['profile'] = 'large'
        params['filter'] = 'movie'
        params['striptags'] = 'synopsis,synopsisshort'
        params['format'] = 'json'

        # do the request
        response = self._do_request('movie', params);

        return response;

    def tvseries(self, id):
        """Get the TVshow details by ID"""
        # build the params
        params = {}
        params['partner'] = self._partner_key
        params['code'] = id
        params['profile'] = 'large'
        params['striptags'] = 'synopsis,synopsisshort'
        params['format'] = 'json'

        # do the request
        response = self._do_request('tvseries', params);

        return response;

    def season(self, id):
        """Get the season details by ID"""
        # build the params
        params = {}
        params['partner'] = self._partner_key
        params['code'] = id
        params['profile'] = 'large'
        params['striptags'] = 'synopsis,synopsisshort'
        params['format'] = 'json'

        # do the request
        response = self._do_request('season', params);

        return response;

    def episode(self, id):
        """Get the episode details by ID"""
        # build the params
        params = {}
        params['partner'] = self._partner_key
        params['code'] = id
        params['profile'] = 'large'
        params['striptags'] = 'synopsis,synopsisshort'
        params['format'] = 'json'

        # do the request
        response = self._do_request('season', params);

        return response;
