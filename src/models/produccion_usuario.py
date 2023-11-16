from config_db import db, ma, app
from sqlalchemy import text
from marshmallow import fields

class UsuarioProduccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primer_nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    nombre = db.Column(db.String(50))
    compensacion_unidad = db.Column(db.Float)
    compensacion_paquete = db.Column(db.Float)
    cantidad_total = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)
    precio = db.Column(db.Integer)
    nombre_rol = db.Column(db.String(50))

    def __init__(self,primer_nombre,apellido,nombre,compensacion_unidad,compensacion_paquete,cantidad_total,fecha,precio,nombre_rol):
        self.primer_nombre = primer_nombre
        self.apellido = apellido
        self.nombre = nombre
        self.compensacion_unidad = compensacion_unidad
        self.compensacion_paquete = compensacion_paquete
        self.cantidad_total = cantidad_total
        self.fecha = fecha
        self.precio = precio
        self.nombre_rol = nombre_rol
    
    def calculo_paquete(production):
        new = {}

        precioPaquete = 12 * production['precio']

        compensacionPaquete = precioPaquete * (production['compensacion_paquete'] / 100)

        new['compensacion'] = compensacionPaquete
        new['precio'] = precioPaquete
        new['nombre'] = production['nombre']
        new['cantidad'] = 12
        new['precio_unidad'] = production['precio']
        new['porcentaje'] = production['compensacion_paquete']
        new['nombre_empleado'] = production['primer_nombre'] + ' ' + production['apellido']
        new['fecha'] = production['fecha']
        new['nombre_rol'] = production['nombre_rol']

        return new
    
    def calculo_unidad(production,remaining):

        new = {}
        remainingPrecio = remaining * production['precio']
        new['compensacion'] = remainingPrecio * (production['compensacion_unidad'] / 100)
        new['precio'] = remainingPrecio
        new['nombre'] = production['nombre']
        new['cantidad'] = remaining
        new['precio_unidad'] = production['precio']
        new['porcentaje'] = production['compensacion_unidad']
        new['nombre_empleado'] = production['primer_nombre'] + ' ' + production['apellido']
        new['fecha'] = production['fecha']
        new['nombre_rol'] = production['nombre_rol']

        return new
    
    def build_final_object(production,final_object,production_object):
        production['compensacion_unidad'] = float(production['compensacion_unidad'])
        production['compensacion_paquete'] = float(production['compensacion_paquete'])
        production['cantidad_total'] = int(production['cantidad_total'])
        production['fecha'] = str(production['fecha'])
        production['precio'] = int(production['precio'])

        if production['cantidad_total'] >= 12:
            new = UsuarioProduccion.calculo_paquete(production)
            final_object.append(new)
            remaining = production['cantidad_total'] % 12

            if remaining > 0:
                new = UsuarioProduccion.calculo_unidad(production,remaining)
                final_object.append(new)

        elif production['cantidad_total'] ==12:
            new = UsuarioProduccion.calculo_paquete(production)
            final_object.append(new)
        else:
            remaining = production['cantidad_total']
            new = UsuarioProduccion.calculo_unidad(production,remaining)
            final_object.append(new)
        
        production_object['produccion'] = final_object
    
    def ByUsuario(usuario_id, fecha_inicio, fecha_fin):

        if fecha_inicio == None:
            fecha_inicio = '1900-01-01'
        
        if fecha_fin == None:
            fecha_fin = '2100-01-01'

        result = db.session.execute(text('''SELECT SUM(production.cantidad) AS cantidad_total,
                                            users.primer_nombre, 
                                            users.apellido, 
                                            production.fecha, 
                                            products.nombre,
                                            products.compensacion_unidad, 
                                            products.compensacion_paquete, 
                                            products.precio, MAX(roles.name) AS nombre_rol
                                            FROM production 
                                            JOIN products ON products.id = production.id_producto
                                            JOIN users ON users.id = production.usuario_id 
                                            JOIN roles ON roles.id = users.rol_id
                                            WHERE users.id = :usuario_id AND production.fecha BETWEEN :fecha_inicio AND :fecha_fin
                                            GROUP BY users.primer_nombre, users.apellido, production.fecha, products.nombre, products.id;'''), {'usuario_id': usuario_id,
                                             'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
        
        schema = UsuarioProduccionSchema(many=True)
        produccion_total = schema.dump(result)
        produccion_usuario_object = {}

        objeto_paquete =  []

        for production in produccion_total:
            production['compensacion_unidad'] = float(production['compensacion_unidad'])
            production['compensacion_paquete'] = float(production['compensacion_paquete'])
            production['cantidad_total'] = int(production['cantidad_total'])
            production['fecha'] = str(production['fecha'])
            production['precio'] = int(production['precio'])

            UsuarioProduccion.build_final_object(production,objeto_paquete,produccion_usuario_object)
            produccion_usuario_object['compensacion_total'] = sum([x['compensacion'] for x in objeto_paquete])

        return produccion_usuario_object      

    def Total(fecha_inicio, fecha_fin):

        if fecha_inicio == None:
            fecha_inicio = '1999-01-01'
        
        if fecha_fin == None:
            fecha_fin = '2999-01-01'

        result = db.session.execute(text('''SELECT SUM(production.cantidad) AS cantidad_total,
                                         users.primer_nombre,
                                         users.apellido,
                                         production.fecha,
                                         products.nombre,
                                         products.compensacion_unidad,
                                         products.compensacion_paquete,
                                         products.precio,
                                         roles.name AS nombre_rol

                                         FROM production
                                         JOIN products ON products.id = production.id_producto
                                         JOIN users ON users.id = production.usuario_id
                                         JOIN roles ON roles.id = users.rol_id
                                         WHERE production.fecha BETWEEN :fecha_inicio AND :fecha_fin

                                         GROUP BY users.primer_nombre, users.apellido, production.fecha, products.nombre, products.id, roles.name;'''), {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
        
        schema = UsuarioProduccionSchema(many=True)
        produccion_total = schema.dump(result)
        produccion_object = {}
        objeto_paquete = []

        for production in produccion_total:
            UsuarioProduccion.build_final_object(production,objeto_paquete,produccion_object)
        
        return produccion_object


class UsuarioProduccionSchema(ma.Schema):
    id = fields.Integer(allow_none=False)
    primer_nombre = fields.Str(required=True, allow_none=False)
    apellido = fields.Str(required=True, allow_none=False)
    nombre = fields.Str(required=True, allow_none=False)
    compensacion_unidad = fields.Float(required=True, allow_none=False)
    compensacion_paquete = fields.Float(required=True, allow_none=False)
    cantidad_total = fields.Integer(required=True, allow_none=False)
    fecha = fields.DateTime(required=True, allow_none=False)
    precio = fields.Integer(required=True, allow_none=False)
    nombre_rol = fields.Str(required=True, allow_none=False)

    class Meta:
        fields = ('id', 'primer_nombre', 'apellido', 'nombre', 'compensacion_unidad', 'compensacion_paquete', 'cantidad_total', 'fecha', 'precio', 'nombre_rol')