from marshmallow import Schema, ValidationError, fields, validate, validates


class BlacklistCreateSchema(Schema):
    email = fields.Email(required=True)
    app_uuid = fields.UUID(required=True)
    blocked_reason = fields.String(required=False, allow_none=True, validate=validate.Length(max=255))


class BlacklistResponseSchema(Schema):
    email = fields.Email(required=True)
    app_uuid = fields.String(required=True)
    blocked_reason = fields.String(allow_none=True)
    request_ip = fields.String(required=True)
    created_at = fields.DateTime(required=True)


class BlacklistLookupSchema(Schema):
    @validates('email')
    def validate_email(self, value):
        if '@' not in value:
            raise ValidationError('Not a valid email address.')
