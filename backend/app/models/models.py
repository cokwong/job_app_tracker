from flask_sqlalchemy import SQLAlchemy, event

db = SQLAlchemy()


class Users(db.Model):
    """
    This models defines the Users table where each row stores a user's information
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    google_id = db.Column(db.String(21), unique=True)
    email = db.Column(db.String(255), unique=True)
    tables = db.relationship('UserApplicationTables', cascade='all, delete', backref='user')

    def __repr__(self):
        return f'<User {self.id}>'


class UserApplicationTables(db.Model):
    """
    This model defines the UserApplicationTables table where each row stores an
    application table associated with a user
    """
    __tablename__ = 'user_application_tables'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(30))
    apps = db.relationship('Applications', cascade='all, delete', backref='table', lazy='dynamic')
    __table_args__ = (db.UniqueConstraint('user_id', 'name'),)

    def __repr__(self):
        return f'<UserApplicationTable {self.id}>'


class Applications(db.Model):
    """
    This model defines the Applications table each row stores information of an
    application associated with a user's application table
    """
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    table_id = db.Column(db.Integer, db.ForeignKey('user_application_tables.id'))
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    url = db.Column(db.String(300))
    status = db.relationship('ApplicationStatus', backref='apps', lazy='dynamic')

    def __repr__(self):
        return f'<Application {self.id}>'


class Status(db.Model):
    """
    This model defines the static Status table where each row stores a status information
    """
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), unique=True)

    def __repr__(self):
        return f'<Status {self.id}>'


class ApplicationStatus(db.Model):
    """
    This model defines the ApplicationStatus table that maps the status information to
    applications
    """
    __tablename__ = 'application_status'
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    __table_args__ = (db.UniqueConstraint('app_id', 'status_id'),)

    def __repr__(self):
        return f'<ApplicationStatus {self.id}'


@event.listens_for(Status.__table__, 'after_create')
def create_status(*args, **kwargs):
    db.session.add(Status(name='Applied'))
    db.session.add(Status(name='Interview'))
    db.session.add(Status(name='Offer'))
    db.session.add(Status(name='Rejected'))
    db.session.add(Status(name='Ghosted'))
    db.session.commit()
