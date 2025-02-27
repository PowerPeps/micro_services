from flask import Flask, request, jsonify

app = Flask(__name__)

stock_livres = {
    "livre1": 5,
    "livre2": 2,
    "livre3": 0
}


@app.route('/stock/<id_livre>', methods=['GET'])
def verifier_stock(id_livre):
    if id_livre in stock_livres:
        return jsonify({"id_livre": id_livre, "stock": stock_livres[id_livre]})
    return jsonify({"message": "Livre introuvable"}), 404


@app.route('/stock/emprunt', methods=['POST'])
def emprunter_livre():
    data = request.json
    id_livre = data.get("id_livre")
    if id_livre in stock_livres and stock_livres[id_livre] > 0:
        stock_livres[id_livre] -= 1
        return jsonify({"message": f"Livre {id_livre} emprunté avec succès", "stock_restant": stock_livres[id_livre]})
    return jsonify({"message": "Livre non disponible"}), 400


@app.route('/stock/retour', methods=['POST'])
def retourner_livre():
    data = request.json
    id_livre = data.get("id_livre")
    if id_livre in stock_livres:
        stock_livres[id_livre] += 1
        return jsonify({"message": f"Livre {id_livre} retourné avec succès", "stock_restant": stock_livres[id_livre]})
    return jsonify({"message": "Livre introuvable"}), 404

@app.route('/stock/ajouter', methods=['POST'])
def ajouter_livre():
    data = request.json
    id_livre = data.get("id_livre")
    quantite = data.get("quantite", 1)  # Quantité par défaut : 1

    if id_livre in stock_livres:
        stock_livres[id_livre] += quantite
        return jsonify({
            "message": f"{quantite} exemplaire(s) ajouté(s) au stock du livre {id_livre}.",
            "stock_total": stock_livres[id_livre]
        })
    else:
        stock_livres[id_livre] = quantite
        return jsonify({
            "message": f"Livre {id_livre} ajouté avec {quantite} exemplaire(s) au stock.",
            "stock_total": stock_livres[id_livre]
        })

if __name__ == '__main__':
    app.run(port=5001)