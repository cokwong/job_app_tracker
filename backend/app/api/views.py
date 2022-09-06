from flask import Blueprint, session, abort, request, jsonify
from app.models import *
from app.auth.decorators import login_required
from .utils import Serialize

serialize = Serialize()
applications = Blueprint('api/user', __name__, url_prefix='/api/user')


def get_user_id():
    """
    Returns user id of client session.

    :return: int
    """
    user_profile = session.get('profile')
    if user_profile:
        google_id = user_profile['id']
        user_id = Users.query.filter_by(google_id=google_id).first().id
        return user_id
    else:
        abort(401)


@applications.route('', methods=['GET'])
@login_required
def get_user():
    return jsonify(session['profile'])


@applications.route('/tables', methods=['GET'])
@applications.route('/tables/<int:id>', methods=['GET'])
@login_required
def get_tables(id=''):
    user_id = get_user_id()
    if id:
        table = UserApplicationTables.query.get_or_404(id=id)
        if table.user_id != user_id:
            abort(403)
        return jsonify(serialize.table(table, include_apps=True))
    else:
        table = UserApplicationTables.query.filter_by(user_id=user_id).all()
        if table:
            return jsonify(serialize.tables(table))
    return jsonify({})


@applications.route('/tables', methods=['POST'])
@login_required
def create_tables():
    user_id = get_user_id()
    data = request.get_json()
    table_name = data.get('name')
    if not table_name:
        abort(400)
    table = UserApplicationTables(user_id=user_id, name=table_name)
    db.session.add(table)
    db.session.commit()
    print(table.user)
    return jsonify(success=True)


@applications.route('/tables/<int:id>', methods=['PUT'])
@login_required
def edit_tables(id):
    user_id = get_user_id()
    data = request.get_json()
    table_name = data.get('name')
    if not table_name:
        abort(400)
    table = UserApplicationTables.query.get_or_404(id)
    if table.user_id != user_id:
        abort(403)
    table.name = table_name
    db.session.commit()
    return jsonify(success=True)


@applications.route('/tables/<int:id>', methods=['DELETE'])
@login_required
def delete_tables(id):
    user_id = get_user_id()
    table = UserApplicationTables.query.get_or_404(id)
    print(table.user_id, user_id)
    if table.user_id != user_id:
        abort(403)
    db.session.delete(table)
    db.session.commit()
    return jsonify(success=True)


@applications.route('/tables/<int:table_id>/applications', methods=['GET'])
@applications.route('/tables/<int:table_id>/applications/<int:app_id>', methods=['GET'])
@login_required
def get_applications(table_id, app_id=''):
    user_id = get_user_id()
    table = UserApplicationTables.query.get_or_404(table_id)
    if table.user_id != user_id:
        abort(403)
    if app_id:
        app = table.apps.filter_by(id=app_id).first()
        if not app:
            abort(404)
        return jsonify(serialize.application(app))
    else:
        return jsonify(serialize.applications(table.apps))


@applications.route('/tables/<int:table_id>/applications', methods=['POST'])
@login_required
def create_applications(table_id):
    user_id = get_user_id()
    data = request.get_json()
    company = data.get('company')
    position = data.get('position')
    url = data.get('url')
    if not (company and position):
        abort(400)
    table = UserApplicationTables.query.get_or_404(table_id)
    if table.user_id != user_id:
        abort(403)
    app = Applications(table_id=table.id, company=company, position=position, url=url)
    table.apps.append(app)
    db.session.commit()
    return jsonify(success=True)


@applications.route('/tables/<int:table_id>/applications/<int:app_id>', methods=['PUT'])
@login_required
def edit_applications(table_id, app_id):
    user_id = get_user_id()
    data = request.get_json()
    company = data.get('company')
    position = data.get('position')
    url = data.get('url')
    if not (company and position):
        abort(400)
    table = UserApplicationTables.query.get_or_404(table_id)
    if table.user_id != user_id:
        abort(403)
    app = table.apps.filter_by(id=app_id).first()
    if not app:
        abort(404)
    app.company = company
    app.position = position
    app.url = url
    db.session.commit()
    return jsonify(success=True)


@applications.route('/tables/<int:table_id>/applications/<int:app_id>', methods=['PUT'])
@login_required
def delete_applications(table_id, app_id):
    user_id = get_user_id()
    table = UserApplicationTables.query.get_or_404(table_id)
    if table.user_id != user_id:
        abort(403)
    app = table.apps.filter_by(id=app_id).first()
    if not app:
        abort(404)
    db.session.delete(app)
    db.session.commit()
    return jsonify(success=True)


@applications.route('/tables/<int:table_id>/applications/<int:app_id>/status', methods=['PUT'])
@login_required
def set_application_status(table_id, app_id):
    user_id = get_user_id()
    data = request.get_json()
    status_id = data.get('status_id')
    if not status_id:
        abort(400)
    table = UserApplicationTables.query.get_or_404(table_id)
    if table.user_id != user_id:
        abort(403)
    app = table.apps.filter_by(id=app_id).first()
    if not app:
        abort(404)
    app_status = ApplicationStatus(app_id=app.id, status_id=status_id)
    app.status.append(app_status)
    db.session.commit()
    return jsonify(success=True)
