from config_db import db, ma, app
from .roles import Rol
from sqlalchemy import text
from marshmallow import fields, ValidationError,validates_schema
from ..validations.validation import validate_str,validate_int
from .producto import product_id_validation
from .usuario import no_existe_validation

class Produccion(db.Model):
    __tablename__ = 'production'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer)
    id_producto = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)

    def __init__(self,usuario_id,id_producto,cantidad,fecha):
        self.usuario_id = usuario_id
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.fecha = fecha

    def ByUsuario(usuario_id):
        result = db.session.execute(text(""" SELECT SUM(production.cantidad) AS cantidad_total,
                                         users.primer_nombre, users.apellido, production.fecha,
                                         products.nombre,products.compensacion_unidad,products.compensacion_paquete 

                                         FROM production JOIN products ON products.id = production.id_producto
                                         JOIN users ON users.id = production.usuario_id
                                         WHERE users.id = :usuario_id GROUP BY users.primer_nombre, users.apellido, production.fecha,
                                         products.nombre, products.id"""),{'usuario_id':usuario_id})
        
        return result
    

with app.app_context():
    db.create_all()

class ProduccionSchema(ma.Schema):
    id = fields.Integer(allow_none=False)
    usuario_id = fields.Integer(required=True, allow_none=False, validate =[validate_int,no_existe_validation])
    id_producto = fields.Integer(required=True, allow_none=False, validate =[validate_int,product_id_validation])
    cantidad = fields.Integer(required=True, allow_none=False, validate =[validate_int])
    fecha = fields.DateTime(required=True, allow_none=False)

    class Meta:
        fields = ('id','usuario_id','id_producto','cantidad','fecha')

    @validates_schema(skip_on_field_errors=False)
    def product_and_user_validation(self,data,**kwargs):
        usuario_id = data.get('usuario_id')
        id_producto = data.get('id_producto')

        raw_query = text("SELECT LOWER(tipo) FROM products WHERE id = :id")
        params = {'id': id_producto}
        product_existing = db.session.execute(raw_query, params)
        result1 = product_existing.fetchone()

        raw_query = text("SELECT lower(roles.name) FROM users JOIN roles ON roles.id = users.rol_id WHERE users.id = :id")
        params = {'id': usuario_id}
        user_existing = db.session.execute(raw_query, params)
        result2 = user_existing.fetchone()

        if result1[0] != result2[0]:
            raise ValidationError('El tipo de producto no es valido para el usuario.')