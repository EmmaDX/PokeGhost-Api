from flask import Flask, jsonify, request, Response
from collections import OrderedDict
from data import *
import json

app = Flask(__name__)

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
    

if __name__ == '__main__':
    app.run(debug = True)