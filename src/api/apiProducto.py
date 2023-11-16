from flask import Blueprint, request, jsonify
from config_db import db
from ..models.producto import Producto, ProductoSchema

producto_routes = Blueprint("producto_routes", __name__)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

#get
@producto_routes.route("/productos", methods=["GET"])
def producto_list():
    resultall = Producto.query.all()
    total_productos = productos_schema.dump(resultall)
    return jsonify(total_productos)

#get by id
@producto_routes.route("/productos/<int:id>", methods=["GET"])
def producto_by_id(id):
    result = Producto.query.get(id)
    return producto_schema.jsonify(result)

#post
@producto_routes.route("/productos", methods=["POST"])
def create_producto():
    json_data = request.json
    errs = producto_schema.validate(json_data)

    if errs:
        return {"error": errs}, 422
    
    result = Producto(json_data['nombre'], json_data['precio'], json_data['compensacion_unidad'], json_data['compensacion_paquete'],json_data['tipo'])
    db.session.add(result)
    db.session.commit()
    return producto_schema.jsonify(result)

#put
@producto_routes.route("/productos/<int:id>", methods=["PUT"])
def producto_update(id):
    json_data = request.json
    errs = producto_schema.validate(json_data)

    if errs:
        return {"error": errs}, 422
    
    result = Producto.query.get(id)
    result.nombre = json_data['nombre']
    result.precio = json_data['precio']
    result.compensacion_unidad = json_data['compensacion_unidad']
    result.compensacion_paquete = json_data['compensacion_paquete']
    result.tipo = json_data['tipo']
    db.session.commit()
    return producto_schema.jsonify(result)

#delete
@producto_routes.route("/productos/<int:id>", methods=["DELETE"])
def producto_delete(id):
    result = Producto.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return producto_schema.jsonify(result)
