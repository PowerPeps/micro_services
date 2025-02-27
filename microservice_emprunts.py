from flask import Flask, request, jsonify

app = Flask(__name__)

emprunts = {}


@app.route('/emprunt', methods=['POST'])
def enregistrer_emprunt():
    data = request.json
    id_livre = data.get("id_livre")
    utilisateur = data.get("utilisateur")

    if utilisateur not in emprunts:
        emprunts[utilisateur] = []
    emprunts[utilisateur].append(id_livre)

    return jsonify({"message": f"Livre {id_livre} emprunté par {utilisateur}", "emprunts": emprunts[utilisateur]})


@app.route('/emprunts/<utilisateur>', methods=['GET'])
def lister_emprunts(utilisateur):
    if utilisateur in emprunts:
        return jsonify({"utilisateur": utilisateur, "emprunts": emprunts[utilisateur]})
    return jsonify({"message": "Aucun emprunt pour cet utilisateur"}), 404


if __name__ == '__main__':
    app.run(port=5002)