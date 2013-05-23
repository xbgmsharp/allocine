import pprint
from allocine import allocine

api = allocine()
api.configure('100043982026','29d185d98c984a359e6e6f26a0474269')

search = api.search("Fight club", "movie")
print "Search result Count [{0}] Code [{1}] Title [{2}]".format(search['feed']['totalResults'],
                                                                search['feed']['movie'][0]['code'],
                                                                search['feed']['movie'][0]['originalTitle'])

movie = api.movie(27405)
print "Movie Title [{0}]".format(movie['movie']['originalTitle'])

serie = api.tvseries(223)
print "Serie Title [{0}]".format(serie['tvseries']['originalTitle'])

season = api.season(12277)
print "Season Number [{0}]".format(season['season']['seasonNumber'])

episode = api.episode(247699)
print "Episode Number [{0}] Title [{1}]".format(episode['episode']['episodeNumberSeason'], episode['episode']['originalTitle'])
