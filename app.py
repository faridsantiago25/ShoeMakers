from src.api.apiUsuario import usuario_routes
from src.api.apiProducto import producto_routes
from src.api.apiProduccion import produccion_routes
from src.api.apiRol import rol_routes
from src.api.auth import auth_routes
from config_db import app

from dotenv import load_dotenv
from flask_cors import CORS
from flask import request, jsonify
from internal.auth import validate_token

app.register_blueprint(auth_routes)

@usuario_routes.before_request
@producto_routes.before_request
@produccion_routes.before_request
@rol_routes.before_request

def search_if_logged():
    request_params = request.args

    if request_params.get('Authorization') == None:
        response = jsonify({"message": "No se ha encontrado el token"})
        response.status_code = 401
        return response
    
    token = request_params.get('Authorization').split(" ")[1]
    return validate_token(token,output=True)

app.register_blueprint(usuario_routes)
app.register_blueprint(producto_routes)
app.register_blueprint(produccion_routes)
app.register_blueprint(rol_routes)

CORS(app,resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True, port=8080, host="0.0.0.0")