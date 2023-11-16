from flask import Blueprint, request, jsonify
from config_db import db
from ..models.produccion import Produccion, ProduccionSchema
from ..models.produccion_usuario import UsuarioProduccion, UsuarioProduccionSchema
from sqlalchemy import text


produccion_routes = Blueprint("produccion_routes", __name__)
produccion_schema = ProduccionSchema()
producciones_schema = ProduccionSchema(many=True)

#get 
@produccion_routes.route("/produccion", methods=["GET"])
@produccion_routes.route("/produccion/<int:id>", methods=["GET"])

def produccion_list(usuario_id=None):
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    if usuario_id == None:
        result_all = UsuarioProduccion.Total(fecha_inicio, fecha_fin)
        return jsonify(result_all)
    
    result_all = UsuarioProduccion.ByUsuario(usuario_id, fecha_inicio, fecha_fin)
    return jsonify(result_all)

#get all 
@produccion_routes.route("/produccion/total", methods=["GET"])
def produccion_total():
    result = db.session.execute(text(""" SELECT
                                         production.id,
                                         users.primer_nombre,
                                         users.apellido,
                                         roles.name AS nombre_rol,
                                         cantidad,
                                         production.fecha,
                                         production.id_producto,
                                         production.usuario_id,
                                         products.nombre AS nombre_producto
                                         
                                         FROM production 
                                         JOIN products ON products.id = production.id_producto
                                         JOIN users ON users.id = production.usuario_id
                                         JOIN roles ON roles.id = users.rol_id """))
    
    result = result.fetchall()

    json = []

    for produccion in result:
        new = {
            "id": produccion[0],
            "primer_nombre": produccion[1],
            "apellido": produccion[2],
            "nombre_rol": produccion[3],
            "cantidad": produccion[4],
            "fecha": produccion[5],
            "id_producto": produccion[6],
            "usuario_id": produccion[7],
            "nombre_producto": produccion[8]
        }
        json.append(new)

    return jsonify(json)

#get by id
@produccion_routes.route("/produccion/total/<int:id>", methods=["GET"])

def produccion_total_by_id(id):

    result = db.session.execute(text(""" SELECT production.id,
                                     users.primer_nombre, 
                                     users.apellido,
                                     roles.name AS nombre_rol,
                                     cantidad,
                                     production.fecha,
                                     production.id_producto,
                                     production.usuario_id,
                                     products.nombre AS nombre_producto
                                     
                                     FROM production
                                     JOIN products ON products.id = production.id_producto
                                     JOIN users ON users.id = production.usuario_id
                                     JOIN roles ON roles.id = users.rol_id
                                     WHERE production.id = :id """), {"id": id})
    
    result = result.fetchone()

    json = {
        "id": result[0],
        "primer_nombre": result[1],
        "apellido": result[2],
        "nombre_rol": result[3],
        "cantidad": result[4],
        "fecha": result[5],
        "id_producto": result[6],
        "usuario_id": result[7],
        "nombre_producto": result[8]
    }
    
    return jsonify(json)

#post
@produccion_routes.route("/produccion", methods=["POST"])
def create_produccion():
    json_data = request.json
    errs = produccion_schema.validate(json_data)

    if errs:
        return {"error": errs}, 422
    
    result = Produccion(json_data['usuario_id'], json_data['id_producto'], json_data['cantidad'], json_data['fecha'])
    db.session.add(result)
    db.session.commit()
    return produccion_schema.jsonify(result)

#put
@produccion_routes.route("/produccion/<int:id>", methods=["PUT"])
def produccion_update(id):
    json_data = request.json
    errs = produccion_schema.validate(json_data)

    if errs:
        return {"error": errs}, 422
    
    result = Produccion.query.get(id)
    result.usuario_id = json_data['usuario_id']
    result.id_producto = json_data['id_producto']
    result.cantidad = json_data['cantidad']
    result.fecha = json_data['fecha']

    db.session.commit()
    return produccion_schema.jsonify(result)

#delete
@produccion_routes.route("/produccion/<int:id>", methods=["DELETE"])
def produccion_delete(id):
    result = Produccion.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return produccion_schema.jsonify(result)