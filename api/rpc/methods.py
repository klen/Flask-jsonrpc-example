from flask import session, current_app
from flaskext.principal import identity_changed, Identity
from flaskext.wtf import ValidationError

from api.extensions import db
from api.forms import SignupForm, LoginForm
from api.models import User


def echo(message):
    return message


def signup(**userdata):
    form = SignupForm(**userdata)
    if form.validate():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return 'User created # %s' % user.id
    raise ValidationError(str(form.errors))


def authenticate(**userdata):
    form = LoginForm(**userdata)
    if form.validate():
        user, authenticated = User.query.authenticate(form.username.data, form.password.data)
        if user and authenticated:
            session.permanent = True
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
            return 'User authenticate'
        else:
            raise ValidationError('Invalid login')
    raise ValidationError(str(form.errors))
