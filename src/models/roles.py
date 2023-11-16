from config_db import db, ma, app
from marshmallow import fields,ValidationError
from ..validations.validation import validate_str
from sqlalchemy import text 

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

with app.app_context():
    db.create_all()

def name_validation(val):

    val = val.lower()
    raw_query = text("SELECT EXISTS(SELECT 1 FROM roles WHERE LOWER(name) = :name)")
    params = {'name': val}

    rol_exists = db.session.execute(raw_query, params)
    row = rol_exists.fetchone()

    if row[0] == 1:
        raise ValidationError('El rol ya existe.')
    
class RolSchema(ma.Schema):
    id = fields.Integer(allow_none=True)
    name = fields.Str(required=True, allow_none=False, validate=[validate_str, name_validation])

    class Meta:
        fields = ('id', 'name')
