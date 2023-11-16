from config_db import db, ma, app
from marshmallow import fields, ValidationError
from ..validations.validation import validate_str,validate_int,validate_float
from sqlalchemy import text

class Producto(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    precio = db.Column(db.Integer)
    compensacion_unidad = db.Column(db.Float)
    compensacion_paquete = db.Column(db.Float)
    tipo = db.Column(db.String(50))

    def __init__(self,nombre,precio,compensacion_unidad,compensacion_paquete,tipo):
        self.nombre = nombre
        self.precio = precio
        self.compensacion_unidad = compensacion_unidad
        self.compensacion_paquete = compensacion_paquete
        self.tipo = tipo

with app.app_context():
    db.create_all()

def product_validation(val):
    #check if producto exist 

    val = val.lower()
    raw_query = text("SELECT EXISTS(SELECT 1 FROM products WHERE LOWER(nombre) = :nombre)")
    params = {'nombre': val}

    producto_existing = db.session.execute(raw_query, params)
    row = producto_existing.fetchone()

    if row[0] == 1:
        raise ValidationError('El producto ya existe.')


def product_id_validation(val):
    #check if id product exist
    raw_query = text("SELECT EXISTS(SELECT 1 FROM products WHERE id = :id)")
    params = {'id': val}

    producto_existing = db.session.execute(raw_query, params)
    row = producto_existing.fetchone()

    if row[0] == 0:
        raise ValidationError('El producto no existe.')
    
def tipo_validation(val):

    val = val.lower()
    if val != 'ensamblador' and val != 'cortador' and val != 'guarnecedor':
        raise ValidationError('El tipo de producto no es valido.')

class ProductoSchema(ma.Schema):
    id = fields.Integer(allow_none=False)
    nombre = fields.Str(required=True,allow_none=False, validate= [validate_str,product_validation])
    precio = fields.Integer(required=True, allow_none=False, validate = validate_int)
    compensacion_unidad = fields.Float(required=True, allow_none=False, validate = validate_float)
    compensacion_paquete = fields.Float(required=True, allow_none=False, validate = validate_float)
    tipo = fields.Str(required=True, allow_none=False, validate=[validate_str,tipo_validation])

    class Meta:
        fields = ('id','nombre','precio','compensacion_unidad','compensacion_paquete','tipo')