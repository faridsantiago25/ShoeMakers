from flask import Blueprint, request, jsonify
from internal.auth import write_token, validate_token
from config_db import db
from sqlalchemy import text

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login", methods=["POST"])

def login():
    data = request.get_json()
    id = data['id']

    if id == "":
        response = jsonify({"message": "El id es invalido"})
        response.status_code = 400
        return response
    
    result = db.session.execute(text(""" SELECT users.id, users.primer_nombre, users.apellido, roles.name 
                                     FROM users JOIN roles ON roles.id = users.rol_id WHERE users.id = :id"""), {'id': id})
    
    result = result.fetchone()

    if result == None:
        response = jsonify({"message": "El usuario no existe"})
        response.status_code = 404
        return response
    
    payload = {
        "id": result[0],
        "primer_nombre": result[1],
        "apellido": result[2],
        "rol": result[3]
    }
    return jsonify(write_token(payload).decode('UTF-8'))

@auth_routes.route("/verify/token")
def verify_token():
    token = request.headers.get('Authorization').split(" ")[1]
    return validate_token(token, output=True)