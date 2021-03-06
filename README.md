# Flask-RESTly

[![Build Status](https://travis-ci.org/gorzechowski/flask-restly.svg?branch=master)](https://travis-ci.org/gorzechowski/flask-restly)
[![Latest version](https://img.shields.io/pypi/v/flask-restly.svg)](https://pypi.org/project/flask-restly)
[![Python versions](https://img.shields.io/pypi/pyversions/flask-restly.svg)](https://pypi.org/project/flask-restly)
[![Coverage Status](https://coveralls.io/repos/github/gorzechowski/flask-restly/badge.svg?branch=master)](https://coveralls.io/github/gorzechowski/flask-restly?branch=master)

## Quick start

```
pip install flask-restly
```

By default `flask-restly` uses JSON serializer.

```python
from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get, delete


app = Flask(__name__)

rest = FlaskRestly(app)
rest.init_app(app)


@resource(name='employees')
class EmployeesResource:
    @get('/<id>')
    def get_employee(self, id):
        return dict(id=int(id))

    @get('/')
    def get_employees(self):
        return dict(entites=[
            dict(id=1),
            dict(id=2)
        ])

    @delete('/<id>')
    def delete_employee(self, **kwargs):
        return


with app.app_context():
    EmployeesResource()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
```

```bash
$ python main.py
* Serving Flask app "main" (lazy loading)
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: on
* Restarting with stat
* Debugger is active!
* Debugger PIN: 210-167-642
* Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)
```

## Features

* Decorators-based routing
* JSON and Protobuf built-in serialization
* Custom serializer support
* Authorization and authentication decorators
* Automatic REST-like response codes
* API versioning
* Rating limits

## Todo

* HATEOAS/HAL

## Usage

Please see [examples](/examples) for more details.

### Settings

| Name                                                          | Default value                |
| -----------------------------------------------------------:  | :--------------------------- |
| RESTLY_SERIALIZER: `<flask_restly.serializer.SerializerBase>` | flask_restly.serializer.json |
| RESTLY_API_PREFIX: `<str>`                                    | /api/rest                    |
| RESTLY_PROTOBUF_MIMETYPE: `<str>`                             | application/x-protobuf       |
| RESTLY_RATE_LIMIT_REQUESTS_AMOUNT: `<int>`                    | 100                          |
| RESTLY_RATE_LIMIT_WINDOW_SECONDS: `<int>`                     | 60                           |

### Docs

* [Authentication](/docs/Authentication.md)
* [Authorization](/docs/Authorization.md)
* [Decorators](/docs/Decorators.md)
* [Exceptions](/docs/Exceptions.md)
* [Protobuf](/docs/Protobuf.md)
* [RateLimits](/docs/RateLimits.md)
