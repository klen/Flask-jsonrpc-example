from datetime import datetime
from flaskext.sqlalchemy import BaseQuery
from werkzeug.security import generate_password_hash, check_password_hash

from api.extensions import db


class UserQuery(BaseQuery):

    def from_identity(self, identity):
        try:
            identity.user = self.get(int(identity.name))
        except ValueError:
            identity.user = None

        return identity.user

    def authenticate(self, login, password):

        user = self.filter(db.or_(User.username==login, User.email==login)).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated


class User(db.Model):

    query_class = UserQuery

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(60), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    _password = db.Column("password", db.String(80))

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<%s>" % self

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym("_password",
            descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)
