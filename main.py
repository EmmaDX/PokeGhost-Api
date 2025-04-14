from flask import Flask, jsonify, request, Response
from collections import OrderedDict
from data import *
import json
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": "Algo salio mal en el servidor.", "detalle": str(e)}), 500

@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "El recurso solicitado no fue encontrado."}), 404

@app.route('/')
def root():
    return "Home"

'''
GET -> obtener informacion
POST -> crear informacion
PUT -> actualizar informacion
DELETE -> informacion
'''

#METODOS GET
@app.route("/pokemons", methods = ["GET"])
def get_all():
    return Response(json.dumps(ghost_pokemons, ensure_ascii=False), mimetype='application/json')

@app.route("/pokemons/<int:poke_id>", methods = ["GET"])
def get_by_id(poke_id):
    poke = next((p for p in ghost_pokemons if p["id"] == poke_id), None)
    if poke is None:
        return jsonify({"error": "Pokemon no encontrado"}), 404
    return Response(json.dumps(poke, ensure_ascii=False), mimetype='application/json'), 200

@app.route("/pokemons/<string:poke_name>", methods = ["GET"])
def get_by_name(poke_name):
    poke = next((p for p in ghost_pokemons if p["name"].lower() == poke_name.lower()), None)
    if poke is None:
        return jsonify({"error": "Pokemon no encontrado"}), 404
    return Response(json.dumps(poke, ensure_ascii=False), mimetype='application/json'), 200

@app.route("/pokemons/firstType/<string:first_Type>", methods = ["GET"])
def get_by_firstType(first_Type):
    filtered_pokes = [p for p in ghost_pokemons if p["primtip"] and p["primtip"].lower() == first_Type.lower()]
    if not filtered_pokes:
        return jsonify({"error": "No se encontraron Pokémon con ese tipo primario."}), 404
    return Response(json.dumps(filtered_pokes, ensure_ascii=False), mimetype='application/json'), 200
    
@app.route("/pokemons/secType/<string:sec_Type>", methods = ["GET"])
def get_by_secType(sec_Type):
    filtered_pokes = [p for p in ghost_pokemons if p["segtip"] and p["segtip"].lower() == sec_Type.lower()]
    if not filtered_pokes:
        return jsonify({"error": "No se encontraron Pokémon con ese tipo secundario."}), 404
    return Response(json.dumps(filtered_pokes, ensure_ascii=False), mimetype='application/json'), 200

#METODO POST
@app.route("/pokemons", methods=["POST"])
def create_pokemon():
    new_poke = request.json
    print(new_poke)
    required_fields = ["id", "name", "clasificacion", "primtip", "segTip", "image"]
    if not all(field in new_poke for field in required_fields):
        return jsonify({"error": "Datos inválidos. Debe incluir todos los datos necesarios"}), 400
    ghost_pokemons.append(new_poke)
    return jsonify({"message": "Pokémon creado exitosamente."}), 201

#METODO PUT
@app.route("/pokemons/<int:poke_id>", methods=["PUT"])
def update_pokemon(poke_id):
    updated_data = request.json
    valid_fields = ["name", "clasificacion", "primtip", "segtip", "image"]

    # Buscar el Pokémon por ID
    poke = next((p for p in ghost_pokemons if p["id"] == poke_id), None)
    if poke is None:
        return jsonify({"error": "Pokemon no encontrado"}), 404

    # Validar que los campos enviados sean válidos
    for field in updated_data.keys():
        if field not in valid_fields:
            return jsonify({"error": f"El campo '{field}' no es válido para actualizar."}), 400

    # Actualizar el Pokémon
    poke.update(updated_data)
    return jsonify({"message": "Pokémon actualizado exitosamente.", "pokemon": poke}), 200

#METODO DELETE
@app.route("/pokemons/<int:poke_id>", methods=["DELETE"])
def delete_pokemon(poke_id):
    poke = next((p for p in ghost_pokemons if p["id"] == poke_id), None)
    if poke is None:
        return jsonify({"error": "Pokemon no encontrado"}), 404
    ghost_pokemons.remove(poke)
    return jsonify({"message": "Pokémon eliminado exitosamente."}), 200

if __name__ == '__main__':
    app.run(debug = True)
