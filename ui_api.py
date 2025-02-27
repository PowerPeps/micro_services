from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) #autorise requetes cross origin

MICROSERVICE_STOCKS = "http://127.0.0.1:5001"
MICROSERVICE_EMPRUNTS = "http://127.0.0.1:5002"
MICROSERVICE_RETOURS = "http://127.0.0.1:5003"


@app.route('/action', methods=['POST'])
def effectuer_action():
    # Lecture des données envoyées par le client
    data = request.json
    action = data.get("action")
    id_livre = data.get("id_livre")
    utilisateur = data.get("utilisateur", "anonyme")

    if action == "stock":
        # Vérification du stock
        response = requests.get(f"{MICROSERVICE_STOCKS}/stock/{id_livre}")
        return jsonify(response.json())

    elif action == "emprunt":
        # Emprunter un livre
        stock_response = requests.post(f"{MICROSERVICE_STOCKS}/stock/emprunt", json={"id_livre": id_livre})
        if stock_response.status_code == 200:
            emprunt_response = requests.post(f"{MICROSERVICE_EMPRUNTS}/emprunt",
                                             json={"id_livre": id_livre, "utilisateur": utilisateur})
            return jsonify(emprunt_response.json())
        return jsonify({"message": "Impossible d'emprunter, livre non disponible"})

    elif action == "retour":
        # Retourner un livre
        retour_response = requests.post(f"{MICROSERVICE_STOCKS}/stock/retour", json={"id_livre": id_livre})
        if retour_response.status_code == 200:
            retour_data = {"id_livre": id_livre, "utilisateur": utilisateur}
            requests.post(f"{MICROSERVICE_RETOURS}/retour", json=retour_data)
            return jsonify({"message": f"Livre {id_livre} retourné avec succès"})
        return jsonify({"message": "Erreur lors du retour, livre introuvable"})

    elif action == "ajouter":
        # Ajouter un ou plusieurs livres dans le stock
        quantite = data.get("quantite", 1)
        ajouter_response = requests.post(f"{MICROSERVICE_STOCKS}/stock/ajouter",
                                         json={"id_livre": id_livre, "quantite": quantite})
        return jsonify(ajouter_response.json())

    return jsonify({"message": "Action non reconnue"}), 400


if __name__ == '__main__':
    app.run(port=5000)  # API Gateway sur port 5000