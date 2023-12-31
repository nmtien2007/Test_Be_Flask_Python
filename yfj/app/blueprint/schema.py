from marshmallow import Schema, fields
from app.enums import UserType


class UserSchema(Schema):
    email = fields.Str(required=True)
    user_type = fields.Enum(UserType, by_value=True, required=True)

    class Meta:
        strict = True


class SubjectsSchema(Schema):
    math = fields.Float(required=True, validate=lambda x: -1 < x < 10)
    physics = fields.Float(required=True, validate=lambda x: -1 < x < 10)
    chemistry = fields.Float(required=True, validate=lambda x: -1 < x < 10)
    biology = fields.Float(required=True, validate=lambda x: -1 < x < 10)
    literature = fields.Float(required=True, validate=lambda x: -1 < x < 10)
    history = fields.Float(required=True, validate=lambda x: -1 < x < 10)
    geography = fields.Float(required=True, validate=lambda x: -1 < x < 10)
    philosophy = fields.Float(required=True, validate=lambda x: -1 < x < 10)
    art = fields.Float(required=True, validate=lambda x: -1 < x < 10)
    language = fields.Float(required=True, validate=lambda x: -1 < x < 10)

    class Meta:
        strict = True


class UserScoreSchema(Schema):
    user_id = fields.String(required=True)
    user_type = fields.Enum(UserType, by_value=True, required=True)
    subject_scores = fields.Nested(SubjectsSchema)


class UserScoreUpdateSchema(Schema):
    subject_scores = fields.Nested(SubjectsSchema)


class JobSchema(Schema):
    jobs = fields.List(fields.String, required=True)


class CreateJobSchema(JobSchema):
    pass


class UpdateJobSchema(JobSchema):
    pass
