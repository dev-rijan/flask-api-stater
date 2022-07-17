from dataclasses import Field
from sqlalchemy import String
from webargs import fields
from src.extensions import ma


class FieldsSchema(ma.Schema):
    field_name = fields.List(fields.String())


class UnprocessableEntitySchema(ma.Schema):
    status_code = fields.Integer()
    description = fields.String()
    fields = ma.Nested(FieldsSchema)
