from functools import wraps

def content(func):
    @wraps(func)
    def wrapped():
        return "<div id='content'></div>" + func() + "<hr>"

    return wrapped

