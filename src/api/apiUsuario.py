from flask import request, jsonify, Blueprint
from config_db import db
from ..models.usuario import Usuario, UsuarioSchema
from marshmallow import ValidationError
from sqlalchemy import text
import json

usuario_routes = Blueprint("usuario_routes", __name__)
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

# get
@usuario_routes.route("/usuarios", methods=["GET"])
def usuario_list():
    result = db.session.execute(text(""" SELECT users.id,
                                     users.primer_nombre,
                                     users.apellido,
                                     roles.name AS nombre_rol,
                                     roles.id,
                                     users.activo
                                     FROM users JOIN roles ON roles.id = users.rol_id """))
    
    resultall = result.fetchall()

    all_usuarios = []

    for usuario in resultall:
        json = {
            "id": usuario[0],
            "primer_nombre": usuario[1],
            "apellido": usuario[2],
            "nombre_rol": usuario[3],
            "rol_id": usuario[4],
            "activo": usuario[5]
        } 
        all_usuarios.append(json)

    return jsonify(all_usuarios)

# get by id
@usuario_routes.route("/usuarios/<int:id>", methods=["GET"])

def usuario_by_id(id):

    result = db.session.execute(text(""" SELECT users.id,
                                     users.primer_nombre,
                                     users.apellido,
                                     roles.name AS nombre_rol,
                                     roles.id,
                                     users.activo
                                     FROM users JOIN roles ON roles.id = users.rol_id WHERE users.id = :id """), {"id": id})
    
    result = result.fetchone()

    json = {
        "id": result[0],
        "primer_nombre": result[1],
        "apellido": result[2],
        "nombre_rol": result[3],
        "rol_id": result[4],
        "activo": result[5]
    }

    return jsonify(json)

# post
@usuario_routes.route("/usuarios", methods=["POST"])

def create_usuario():
    json_data = request.json
    errs = usuario_schema.validate(json_data)

    if errs:
        return {"error": errs}, 422
    
    result = Usuario(json_data['id'],json_data['rol_id'],json_data['primer_nombre'],json_data['apellido'])
    db.session.add(result)
    db.session.commit()
    return usuario_schema.jsonify(result)

# put
@usuario_routes.route("/usuarios/<int:id>", methods=["PUT"])

def usuario_update(id):
    json_data = request.json

    result = Usuario.query.get(id)
    result.id = json_data['id']
    result.primer_nombre = json_data['primer_nombre']
    result.apellido = json_data['apellido']
    result.rol_id = json_data['rol_id']
    result.activo = json_data['activo']
    db.session.commit()
    return usuario_schema.jsonify(result)

# delete
@usuario_routes.route("/usuarios/<int:id>", methods=["DELETE"])

def usuario_delete(id):
    result = Usuario.query.get(id)
    result.activo = False
    db.session.commit()
    return usuario_schema.jsonify(result)