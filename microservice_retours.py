from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

retours = []


@app.route('/retour', methods=['POST'])
def enregistrer_retour():
    data = request.json
    id_livre = data.get("id_livre")
    utilisateur = data.get("utilisateur")

    if not id_livre or not utilisateur:
        return jsonify({"message": "Les champs id_livre et utilisateur sont obligatoires."}), 400

    retours.append({"id_livre": id_livre, "utilisateur": utilisateur})
    logging.info(f"Livre {id_livre} retourné par {utilisateur}")
    return jsonify({"message": f"Livre {id_livre} retourné par {utilisateur}", "historique_retours": retours})


@app.route('/retours', methods=['GET'])
def lister_retours():
    return jsonify({"historique_retours": retours})


if __name__ == '__main__':
    app.run(port=5003)