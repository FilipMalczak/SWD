
def cached(foo):
    cache = {}
    def bar(*args):
        if args in cache:
            return cache[args]
        out = foo(*args)
        cache[args] = out
        return out
    return bar