from allocine import allocine
api = allocine()
api.configure('100043982026','29d185d98c984a359e6e6f26a0474269')
movie = api.get(27405)
print movie