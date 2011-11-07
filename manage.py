#!/usr/bin/env python
# coding: utf-8
from flask import current_app
from flaskext.script import Manager, prompt_bool, prompt, prompt_pass
import nose

from api import create_app
from api.extensions import db
from api.models import User


manager = Manager(create_app)


@manager.command
def test():
    nose.run()


@manager.command
def createall():
    "Creates database tables"
    db.create_all()


@manager.command
def dropall():
    "Drops all database tables"
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()


@manager.shell
def make_shell_context():
    return dict(app=current_app,
                db=db,
                User=User)


@manager.option('-u', '--username', dest="username", required=False)
@manager.option('-p', '--password', dest="password", required=False)
@manager.option('-e', '--email', dest="email", required=False)
def createuser(username=None, password=None, email=None):
    "Create a new user"
    if username is None:
        while True:
            username = prompt("Username")
            user = User.query.filter(User.username==username).first()
            if user is not None:
                print "Username %s is already taken" % username
            else:
                break

    if email is None:
        while True:
            email = prompt("Email address")
            user = User.query.filter(User.email==email).first()
            if user is not None:
                print "Email %s is already taken" % email
            else:
                break

    if password is None:
        password = prompt_pass("Password")

        while True:
            password_again = prompt_pass("Password again")
            if password != password_again:
                print "Passwords do not match"
            else:
                break

    user = User(username=username,
                email=email,
                password=password)

    db.session.add(user)
    db.session.commit()

    print "User created with ID", user.id


if __name__ == '__main__':
    manager.run()
