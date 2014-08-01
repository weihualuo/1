

def default_int(v, default=0):
    try:
        return int(v)
    except:
        return default