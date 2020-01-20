#!/usr/bin/env python3
#-*- coding:utf-8 -*-
"""
A module to use Allocine API V3 in Python
Repository: https://github.com/xbgmsharp/allocine
Base on work from: https://github.com/gromez/allocine-api
License: LGPLv2 http://www.gnu.org/licenses/lgpl.html

Sample code:

    from allocine import allocine
    api = allocine()
    api.configure('100043982026','29d185d98c984a359e6e6f26a0474269')
    movie = api.movie(27405)
    search = api.search("Oblivion")

"""
# Debug
#from pprint import pprint
# standard module
from datetime import date
import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error
import hashlib, base64
import json

__version__ = "0.2"
__author__ = "Francois Lacroix"
__license__ = "GPL"
__description__ = "A module to use Allocine API V3 in Python"

class allocine(object):
    """An interface to the Allocine API"""
    def __init__(self, partner_key='aXBob25lLXYy', secret_key='29d185d98c984a359e6e6f26a0474269'):
        """Init values"""
        self._api_url = 'http://api.allocine.fr/rest/v3'
        self._partner_key  = partner_key
        self._secret_key = secret_key
        self._user_agent = 'Mozilla/5.0 (Linux; U; Android 1.9; en-gb) AppleWebKit/999+ (KHTML, like Gecko) Safari/999.9'

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
        to_hash = (self._secret_key + urllib.parse.urlencode(params) + '&sed=' + sed).encode("utf8")
        sha1 = hashlib.sha1(to_hash).digest()
        #print sha1
        b64 = base64.b64encode(sha1)
        #print b64
        sig = urllib.parse.quote(b64)
        query_url += '?'+urllib.parse.urlencode(params, True)+'&sed='+sed+'&sig='+sig
        #query_url += '?'+urllib.parse.urlencode(params, True)
        #print query_url;

        # do the request
        req = urllib.request.Request(query_url)
        req.add_header('User-agent', self._user_agent)

        str_response = urllib.request.urlopen(req, timeout = 10).readline().decode("utf-8")
        response = json.loads(str_response)

        return response;

    def search(self, query, filter="movie"):
        """Search for a term
        Param:
            query -- Term to search for
            filter -- Filter by resut type (movie, theater, person, news, tvseries)
        """
        # build the params
        params = {}
        params['format'] = 'json'
        params['partner'] = self._partner_key
        params['q'] = query
        params['filter'] = filter

        # do the request
        response = self._do_request('search', params);

        return response;

    def movie(self, id, profile="large", mediafmt="mp4-lc:m"):
        """Get the movie details by ID
        Param:
            id -- Unique ID of the movie your search for
            profile -- Level of details to return (small, medium, large)
            mediafmt -- The media format (flv, mp4-lc, mp4-hip, mp4-archive, mpeg2-theater, mpeg2)
        """
        # build the params
        params = {}
        params['format'] = 'json'
        params['partner'] = self._partner_key
        params['mediafmt'] = mediafmt
        params['profile'] = profile
        params['code'] = id
        params['striptags'] = 'synopsis,synopsisshort'

        # do the request
        response = self._do_request('movie', params);

        return response;

    def tvseries(self, id, profile="large", mediafmt="mp4-lc:m"):
        """Get the TVshow details by ID
        Param:
            id -- Unique ID of the tvseries your search for
            profile -- Level of details to return (small, medium, large)
            mediafmt -- The media format (flv, mp4-lc, mp4-hip, mp4-archive, mpeg2-theater, mpeg2)
        """
        # build the params
        params = {}
        params['format'] = 'json'
        params['partner'] = self._partner_key
        params['mediafmt'] = mediafmt
        params['profile'] = profile
        params['code'] = id
        params['striptags'] = 'synopsis,synopsisshort'

        # do the request
        response = self._do_request('tvseries', params);

        return response;

    def season(self, id, profile="large"):
        """Get the season details by ID
        Param:
            id -- Unique ID of the season your search for
            profile -- Level of details to return (small, medium, large)
        """
        # build the params
        params = {}
        params['format'] = 'json'
        params['partner'] = self._partner_key
        params['profile'] = profile
        params['code'] = id
        params['striptags'] = 'synopsis,synopsisshort'

        # do the request
        response = self._do_request('season', params);

        return response;

    def episode(self, id, profile="large"):
        """Get the episode details by ID
        Param:
            id -- Unique ID of the episode your search for
            profile -- Level of details to return (small, medium, large)
        """
        # build the params
        params = {}
        params['format'] = 'json'
        params['partner'] = self._partner_key
        params['profile'] = profile
        params['code'] = id
        params['striptags'] = 'synopsis,synopsisshort'

        # do the request
        response = self._do_request('episode', params);

        return response;
