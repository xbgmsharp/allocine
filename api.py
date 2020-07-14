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
import random, time
import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse
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

    def configure(self, partner_key=None, secret_key=None):
        """Set the keys"""
        self._partner_key = partner_key
        self._secret_key = secret_key

    def _get_random_user_agent(self):
        va = random.randrange(1, 4)
        vb = random.randrange(0, 9)
        a = random.randrange(0, 9)
        b = random.randrange(0, 99)
        c = random.randrange(0, 999)

        userAgents = [f"Mozilla/5.0 (Linux; U; Android {va}.{vb}; fr-fr; Nexus One Build/FRF91) AppleWebKit/5{b}.{c} (KHTML, like Gecko) Version/{a}.{a} Mobile Safari/5{b}.{c}",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}; fr-fr; Dell Streak Build/Donut AppleWebKit/5{b}.{c}+ (KHTML, like Gecko) Version/3.{a}.2 Mobile Safari/ 5{b}.{c}.1",
                    f"Mozilla/5.0 (Linux; U; Android 4.{va}.{vb}; fr-fr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                    f"Mozilla/5.0 (Linux; U; Android 4.{va}.{vb}; fr-fr; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}; en-gb) AppleWebKit/999+ (KHTML, like Gecko) Safari/9{b}.{a}",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}.5; fr-fr; HTC_IncredibleS_S710e Build/GRJ{b}) AppleWebKit/5{b}.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/5{b}.1",
                    f"Mozilla/5.0 (Linux; U; Android 2.{va}.{vb}; fr-fr; HTC Vision Build/GRI{b}) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}.4; fr-fr; HTC Desire Build/GRJ{b}) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                    f"Mozilla/5.0 (Linux; U; Android 2.{va}.{vb}; fr-fr; T-Mobile myTouch 3G Slide Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}.3; fr-fr; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                    f"Mozilla/5.0 (Linux; U; Android 2.{va}.{vb}; fr-fr; HTC_Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari",
                    f"Mozilla/5.0 (Linux; U; Android 2.{va}.{vb}; fr-fr; HTC Pyramid Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/5{b}.1",
                    f"Mozilla/5.0 (Linux; U; Android 2.{va}.{vb}; fr-fr; LG-LU3000 Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/5{b}.1",
                    f"Mozilla/5.0 (Linux; U; Android 2.{va}.{vb}; fr-fr; HTC_DesireS_S510e Build/GRI{a}) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/{c}.1",
                    f"Mozilla/5.0 (Linux; U; Android 2.{va}.{vb}; fr-fr; HTC_DesireS_S510e Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}.3; fr-fr; HTC Desire Build/GRI{a}) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                    f"Mozilla/5.0 (Linux; U; Android 2.{va}.{vb}; fr-fr; HTC Desire Build/FRF{a}) AppleWebKit/533.1 (KHTML, like Gecko) Version/{a}.0 Mobile Safari/533.1",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}; fr-lu; HTC Legend Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/{a}.{a} Mobile Safari/{c}.{a}",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}; fr-fr; HTC_DesireHD_A9191 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}.1; fr-fr; HTC_DesireZ_A7{c} Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/{c}.{a}",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}.1; en-gb; HTC_DesireZ_A7272 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/{c}.1",
                    f"Mozilla/5.0 (Linux; U; Android {va}.{vb}; fr-fr; LG-P5{b} Build/FRG83) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"]

        return userAgents[random.randrange(0, len(userAgents) - 1)]

    def _do_request(self, method=None, params=None):
        """Generate and send the request"""
        response = None

        # build the URL
        query_url = self._api_url+'/'+method

        # new algo to build the query
        today = date.today()
        sed = today.strftime('%Y%m%d')
        # print(sed)
        params['sed'] = sed
        to_hash = (method + urllib.parse.urlencode(params) + self._secret_key).encode("utf8")
        sha1 = hashlib.sha1(to_hash).digest()
        # print(sha1)
        b64 = base64.b64encode(sha1)
        # print(b64)
        params['sig'] = b64
        query_url += '?' + urllib.parse.urlencode(params, True)

        triesmax = 10
        tries = 1
        ok = False
        while not ok and tries < triesmax:
            try:
                # do the request
                req = urllib.request.Request(query_url)
                req.add_header('User-agent', self._get_random_user_agent())

                str_response = urllib.request.urlopen(req, timeout = 10).readline().decode("utf-8")
                response = json.loads(str_response)
                ok = True
            except urllib.request.HTTPError as e:
                #print(e)
                if e.code == 403:
                    tries += 1
                    time.sleep(1)
                else:
                    tries = triesmax

        return response

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
        response = self._do_request('search', params)

        return response

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
        response = self._do_request('movie', params)

        return response

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
        response = self._do_request('tvseries', params)

        return response

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
        response = self._do_request('season', params)

        return response

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
        response = self._do_request('episode', params)

        return response
