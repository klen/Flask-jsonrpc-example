from flask import g
from flaskext.principal import AnonymousIdentity
from flaskext.testing import TestCase as Base, Twill

from api import create_app
from api.config import TestConfig
from api.extensions import db


class TestCase(Base):
    """ Base TestClass for application.
    """
    def __init__(self, *args, **kwargs):
        self.twill = None
        super(TestCase, self).__init__(*args, **kwargs)

    def create_app(self):
        app = create_app(TestConfig())
        self.twill = Twill(app, port=3000)
        return app

    def setUp(self):
        db.create_all()
        g.identity = AnonymousIdentity()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @staticmethod
    def assert_401(response):
        assert response.status_code == 401

    def login(self, **kwargs):
        response = self.client.post("/acct/login/", data=kwargs)
        assert response.status_code in (301, 302)

    def logout(self):
        self.client.get("/auth/logout/")
