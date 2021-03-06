from flask_restly.decorator import resource, get, body, post
from flask_restly.serializer import protobuf, SerializerBase
from flask_restly import FlaskRestly
from flask import Flask, make_response
from tests.fixtures.entity_pb2 import Entity
import pytest


@pytest.mark.parametrize("data,expected_data", [
    (dict(), bytes('{}', 'utf8')),
    (list(), bytes('[]', 'utf8')),
    (dict(id=1), bytes('{"id":1}', 'utf8')),
    (dict(items=[dict(id=1)]), bytes('{"items":[{"id":1}]}', 'utf8')),
])
def test_should_serialize_given_response_to_json(data, expected_data):
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get(self):
            return data

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        data = response.get_data().strip(bytes('\n', 'utf8'))
        assert data == expected_data


@pytest.mark.parametrize("data,expected_data", [
    (dict(), bytes('', 'utf8')),
    (dict(id=1), bytes('\x08\x01', 'utf8')),
])
def test_should_serialize_given_response_to_protobuf(data, expected_data):
    app = Flask(__name__)
    api = FlaskRestly()

    app.config['RESTLY_SERIALIZER'] = protobuf

    api.init_app(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        @body(Entity)
        def get(self):
            return data

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        data = response.get_data().strip(bytes('\n', 'utf8'))
        assert response.headers.get('Content-Type') == 'application/x-protobuf'
        assert data == expected_data


@pytest.mark.parametrize("request_data,expected_data", [
    (bytes('\x08\x01', 'utf8'), bytes('\x08\x01', 'utf8')),
])
def test_should_deserialize_given_request_data_to_dictionary(request_data, expected_data):
    app = Flask(__name__)
    api = FlaskRestly()

    app.config['RESTLY_SERIALIZER'] = protobuf

    api.init_app(app)

    @resource(name='test')
    class SomeResource:
        @post('/')
        @body(incoming=Entity, outgoing=Entity)
        def get(self, body):
            print(body)
            return dict(id=body.get('id'))

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.post('/api/rest/v1/test', data=request_data)
        data = response.get_data()
        assert data == expected_data


def test_should_not_serialize_when_response_object_provided():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get(self):
            res = make_response('some response')
            res.status_code = 201
            return res

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        data = response.get_data()
        assert data == bytes('some response', 'utf8')
        assert response.status_code == 201


def test_should_use_custom_serialize_method_when_provided():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/', serialize=lambda r, _: r.get('foo'))
        def get(self):
            return dict(foo='bar')

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        data = response.get_data()
        assert data == bytes('bar', 'utf8')


def test_should_use_default_serializer_when_custom_serializer_not_provided():
    app = Flask(__name__)

    class SomeSerializer(SerializerBase):
        def serialize(self, response, _):
            return response.get('foo')

        def deserialize(self, request, _):
            pass

    app.config['RESTLY_SERIALIZER'] = SomeSerializer()

    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @get('/')
        def get(self):
            return dict(foo='bar')

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.get('/api/rest/v1/test')
        data = response.get_data()
        assert data == bytes('bar', 'utf8')
