from flask import Flask, request, jsonify
from flask_cors import CORS
from services import user_service, carrito_service, pedido_service, camiseta_service, estampa_service

app = Flask(__name__)
CORS(app)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    rol_id = data.get("rol_id")

    if not all([nombre, correo, contrasena, rol_id]):
        return jsonify({"message": "Faltan campos obligatorios", "success": False}), 400

    result = user_service.register_user(nombre, correo, contrasena, rol_id)
    return jsonify(result)

# === USER ===
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    correo = data.get("correo")
    contrasena = data.get("contrasena")

    if not correo or not contrasena:
        return jsonify({"message": "Campos incompletos", "success": False}), 400

    result = user_service.login_user(correo, contrasena)
    return jsonify(result)

# === CARRITO ===
@app.route("/carrito/guardar", methods=["POST"])
def guardar_carrito():
    data = request.get_json()
    usuario_id = data.get("usuario_id")
    items = data.get("items")

    if not usuario_id or not isinstance(items, list):
        return jsonify({"message": "Faltan datos (usuario_id o items)", "success": False}), 400

    result = carrito_service.guardar_carrito_completo(usuario_id, items)
    return jsonify(result), 201

@app.route("/carrito", methods=["POST"])
def crear_carrito():
    data = request.get_json()
    usuario_id = data.get("usuario_id")
    print("usuario_id recibido:", usuario_id)

    if not usuario_id:
        return jsonify({"message": "Falta usuario_id", "success": False})
    return jsonify(carrito_service.crear_carrito_si_no_existe(usuario_id))

# === PEDIDOS ===
@app.route("/pedido", methods=["POST"])
def crear_pedido():
    data = request.get_json()
    return jsonify(pedido_service.crear_nuevo_pedido(data))

@app.route("/pedidos/<int:usuario_id>", methods=["GET"])
def listar_pedidos(usuario_id):
    return jsonify(pedido_service.obtener_pedidos_usuario(usuario_id))

# === ESTAMPAS ===
@app.route("/estampas", methods=["GET"])
def get_estampas():
    return jsonify(estampa_service.listar_estampas())

@app.route("/estampas", methods=["POST"])
def crear_estampa():
    data = request.get_json()
    return jsonify(estampa_service.registrar_estampa(
        data["titulo"],
        data.get("descripcion", ""),
        data["artista_id"],
        data.get("estado", "activa")
    ))

# === CAMISETAS ===
@app.route("/camisetas", methods=["GET"])
def get_camisetas():
    return jsonify(camiseta_service.listar_camisetas())

@app.route("/camisetas", methods=["POST"])
def crear_camiseta():
    data = request.get_json()
    return jsonify(camiseta_service.registrar_camiseta(
        data["talla"],
        data.get("color", ""),
        data.get("material", ""),
        data["precio"],
        data.get("stock", 0)
    ))

if __name__ == '__main__':
    app.run(debug=True)

