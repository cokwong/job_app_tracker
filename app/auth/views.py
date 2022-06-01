from flask import Blueprint, url_for, session, redirect, abort, request, jsonify, current_app as app
from authlib.integrations.flask_client import OAuth
from authlib.integrations.base_client.errors import MismatchingStateError
from .decorators import login_required
from app.models.models import Users, db

auth = Blueprint('', __name__, url_prefix='')

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs'
)


@app.before_request
def before_request():
    """
    Touch session, resetting session timeout
    """
    session.permanent = True
    app.permanent_session_lifetime = app.config['SESSION_LIFETIME']
    session.modified = True


@auth.route('/')
def index():
    return redirect(app.config['FRONTEND_URL'])


@auth.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_url = url_for('.authorize', _external=True)
    return google.authorize_redirect(redirect_url)


@auth.route('/authorize')
def authorize():
    google = oauth.create_client('google')

    try:
        token = google.authorize_access_token()
    except MismatchingStateError:
        # Error is thrown when session changes during authentication
        return redirect(url_for('.index', _external=True))

    response = google.get('userinfo')
    user_info = response.json()

    # Try to get user from database else add user
    user = Users.query.filter_by(google_id=user_info['id']).first()
    if user:
        if user.email != user_info['email']:
            user.email = user_info['email']
            db.session.commit()
    else:
        user = Users(google_id=user_info['id'], email=user_info['email'])
        db.session.add(user)
        db.session.commit()

    session['profile'] = {'email': user_info['email'], 'id': user_info['id'], 'picture': user_info['picture']}
    return redirect(app.config['FRONTEND_URL'])


@auth.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(app.config['FRONTEND_URL'])
