from flask import json

from api.rpc import mapper
from api.models import User
from api.extensions import db
from tests import TestCase


class TestRpc(TestCase):

    def test_empty(self):
        response = self.client.get('/rpc/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_echo(self):
        data = dict(jsonrpc='2.0', method='api.rpc.methods.echo', params=['Hello!'], id='test')
        result = mapper(data)
        self.assertTrue(result.get('result') == 'Hello!')
        response = self.client.post('/rpc/', data=json.dumps(data), content_type='application/json')
        self.assert200(response)
        self.assertTrue(response.json)
        self.assertTrue(response.json['result'] == 'Hello!')

    def test_signup(self):
        data = dict(
                jsonrpc='2.0',
                method='api.rpc.methods.signup',
                params=dict(
                    username='username',
                    email='email@email.com',
                    password='password',
                ), id='test')
        result = mapper(data)
        self.assertEqual(result.get('result'), 'User created # 1')

        response = self.client.post('/rpc/', data=json.dumps(data), content_type='application/json')
        self.assert200(response)
        self.assertTrue(response.json)
        self.assertTrue(response.json['error'])

        data['params']['username'] = 'username2'
        data['params']['email'] = 'email2@com.com'
        response = self.client.post('/rpc/', data=json.dumps(data), content_type='application/json')
        self.assert200(response)
        self.assertTrue(response.json)
        self.assertTrue(response.json['result'])

    def test_authenticate(self):
        userdata = dict(username='test', email='tester@example.com', password='test')
        user = User(**userdata)
        db.session.add(user)
        db.session.commit()

        data = dict(
                jsonrpc='2.0',
                method='api.rpc.methods.authenticate',
                params=dict(**userdata), id='test')
        result = mapper(data)
        self.assertEqual(result.get('result'), 'User authenticate')

        response = self.client.post('/rpc/', data=json.dumps(data), content_type='application/json')
        self.assert200(response)
        self.assertTrue(response.json)
        self.assertTrue(response.json['result'])
