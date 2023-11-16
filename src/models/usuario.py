from config_db import db, ma, app
from .roles import Rol
from sqlalchemy import text
from marshmallow import fields, ValidationError
from ..validations.validation import validate_str,validate_int

class Usuario(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    rol_id = db.Column(db.Integer)
    primer_nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    activo = db.Column(db.Boolean)

    def __init__(self, id, rol_id, primer_nombre, apellido):
        self.id = id
        self.rol_id = rol_id
        self.primer_nombre = primer_nombre
        self.apellido = apellido
        self.activo = True

with app.app_context():
    db.create_all()

def rol_id_validation(val):
    #check if rol exists

    rol_existing = db.session.query(Rol).filter_by(id=val).first()

    if rol_existing is None:
        raise ValidationError('El rol no existe.')
    
def usuario_id_validation(val):
    #check if usuario exists

    raw_query = text("SELECT EXISTS(SELECT 1 FROM users WHERE id = :id)")
    params = {'id': val}

    usuario_existing = db.session.execute(raw_query, params)
    row = usuario_existing.fetchone()

    if row[0] == 1:
        raise ValidationError('El usuario ya existe.')

def no_existe_validation(val):
    
    raw_query = text("SELECT EXISTS(SELECT 1 FROM users WHERE id = :id)")
    params = {'id': val}

    usuario_existing = db.session.execute(raw_query, params)
    row = usuario_existing.fetchone()

    if row[0] == 0:
        raise ValidationError('El usuario no existe.')

class UsuarioSchema(ma.Schema):
    id = fields.Integer(required=True, allow_none=False, validate =[validate_int, usuario_id_validation])
    rol_id = fields.Integer(required=True, allow_none=False, validate =[validate_int, rol_id_validation])
    primer_nombre = fields.Str(required=True, allow_none=False, validate=validate_str)
    apellido = fields.Str(required=True, allow_none=False, validate=validate_str)
    activo = fields.Boolean(allow_none=True,default=True)

    class Meta:
        fields = ('id', 'rol_id', 'primer_nombre', 'apellido', 'activo')