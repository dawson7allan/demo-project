from marshmallow import Schema, fields


# Need this scheme to serialze sqlalchemy object to JSON
class ProductSchema(Schema):
    id = fields.Int()
    date_time = fields.DateTime()
    description = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    elevation = fields.Int()