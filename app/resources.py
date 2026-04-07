from marshmallow import ValidationError
from flask import request
from flask_restful import Resource

from app.auth import require_bearer_token
from app.extensions import db
from app.models import BlacklistEntry
from app.schemas import BlacklistCreateSchema


create_schema = BlacklistCreateSchema()


def _request_ip():
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.remote_addr or 'unknown'


class HealthResource(Resource):
    def get(self):
        return {'status': 'ok'}, 200


class BlacklistCollectionResource(Resource):
    method_decorators = [require_bearer_token]

    def post(self):
        payload = request.get_json(silent=True) or {}

        try:
            validated = create_schema.load(payload)
        except ValidationError as exc:
            return {
                'message': 'Validation error',
                'errors': exc.messages,
            }, 400

        email = validated['email'].strip().lower()
        existing_entry = BlacklistEntry.query.filter_by(email=email).first()
        if existing_entry:
            return {
                'message': 'Email already exists in blacklist',
                'email': email,
            }, 409

        blacklist_entry = BlacklistEntry(
            email=email,
            app_uuid=str(validated['app_uuid']),
            blocked_reason=validated.get('blocked_reason'),
            request_ip=_request_ip(),
        )

        db.session.add(blacklist_entry)
        db.session.commit()

        return {
            'message': 'Email added to blacklist',
            'data': {
                'email': blacklist_entry.email,
                'app_uuid': blacklist_entry.app_uuid,
                'blocked_reason': blacklist_entry.blocked_reason,
                'request_ip': blacklist_entry.request_ip,
                'created_at': blacklist_entry.created_at.isoformat() + 'Z',
            },
        }, 201


class BlacklistDetailResource(Resource):
    method_decorators = [require_bearer_token]

    def get(self, email):
        normalized_email = email.strip().lower()
        entry = BlacklistEntry.query.filter_by(email=normalized_email).first()

        if not entry:
            return {
                'email': normalized_email,
                'is_blacklisted': False,
                'blocked_reason': None,
            }, 200

        return {
            'email': entry.email,
            'is_blacklisted': True,
            'blocked_reason': entry.blocked_reason,
        }, 200
