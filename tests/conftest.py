import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import os

import pytest

os.environ['AUTH_TOKEN'] = 'test-token'

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    application = create_app('testing')
    with application.app_context():
        db.drop_all()
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers():
    return {
        'Authorization': 'Bearer test-token',
        'Content-Type': 'application/json',
    }
