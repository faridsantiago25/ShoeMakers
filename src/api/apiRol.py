from flask import Blueprint, request, jsonify
from config_db import db
from ..models.roles import Rol, RolSchema

rol_routes = Blueprint("rol_routes", __name__)
rol_schema = RolSchema()
rol_schemas = RolSchema(many=True)

#get
@rol_routes.route("/roles", methods=["GET"])
def rol_list():
    resultall = Rol.query.all()
    total_usuarios = rol_schemas.dump(resultall)
    return jsonify(total_usuarios)

#get by id
@rol_routes.route("/roles/<int:id>", methods=["GET"])
def rol_by_id(id):
    result = Rol.query.get(id)
    return rol_schema.jsonify(result)

#post
@rol_routes.route("/roles", methods=["POST"])
def create_rol():
    json_data = request.json
    errs = rol_schema.validate(json_data)

    if errs:
        return {"error": errs}, 422
    
    result = Rol(json_data['name'])
    db.session.add(result)
    db.session.commit()
    return rol_schema.jsonify(result)

#put
@rol_routes.route("/roles/<int:id>", methods=["PUT"])
def rol_update(id):
    json_data = request.json
    errs = rol_schema.validate(json_data)

    if errs:
        return {"error": errs}, 422
    
    result = Rol.query.get(id)
    result.name = json_data['name']
    db.session.commit()
    return rol_schema.jsonify(result)

#delete
@rol_routes.route("/roles/<int:id>", methods=["DELETE"])
def rol_delete(id):
    result = Rol.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return rol_schema.jsonify(result)