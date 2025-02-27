from flask import Flask, request, jsonify

app = Flask(__name__)

retours = []


@app.route('/retour', methods=['POST'])
def enregistrer_retour():
    data = request.json
    id_livre = data.get("id_livre")
    utilisateur = data.get("utilisateur")

    retours.append({"id_livre": id_livre, "utilisateur": utilisateur})
    return jsonify({"message": f"Livre {id_livre} retourné par {utilisateur}", "historique_retours": retours})


@app.route('/retours', methods=['GET'])
def lister_retours():
    return jsonify({"historique_retours": retours})


if __name__ == '__main__':
    app.run(port=5003)