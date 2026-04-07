from flask import Flask, jsonify
from flask_restful import Api

from app.config import config_by_name
from app.extensions import db, ma, jwt
from app.resources import BlacklistCollectionResource, BlacklistDetailResource, HealthResource


def create_app(config_name=None):
    app = Flask(__name__)
    selected_config = config_name or 'default'
    app.config.from_object(config_by_name[selected_config])

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    api.add_resource(HealthResource, '/health')
    api.add_resource(BlacklistCollectionResource, '/blacklists')
    api.add_resource(BlacklistDetailResource, '/blacklists/<string:email>')

    @app.route('/')
    def index():
        return jsonify({
            'service': 'blacklist-service',
            'status': 'ok',
            'health': '/health'
        })

    with app.app_context():
        db.create_all()

    return app
