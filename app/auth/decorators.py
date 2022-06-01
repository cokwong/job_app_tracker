from flask import session, redirect, url_for, abort
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('profile', None)
        print(user)
        if user:
            return f(*args, **kwargs)
        abort(401)
    return decorated_function
