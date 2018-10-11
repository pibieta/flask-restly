from flask_restly.decorator import resource, put
from flask_restly import FlaskRestly
from flask import Flask


def test_should_return_201_code_when_content_provided_and_code_not_provided():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @put('/')
        def replace(self):
            return dict()

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.put('/api/rest/v1/test', data=dict())
        assert response.status_code == 201
        assert response.get_json() == {}


def test_should_return_custom_200_code_when_content_and_code_provided():
    app = Flask(__name__)
    FlaskRestly(app)

    @resource(name='test')
    class SomeResource:
        @put('/')
        def replace(self):
            return dict(), 200

    with app.app_context():
        SomeResource()

    with app.test_client() as client:
        response = client.put('/api/rest/v1/test', data=dict())
        assert response.status_code == 200
        assert response.get_json() == {}
