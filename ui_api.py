from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)  # Autorise les requêtes Cross-Origin
logging.basicConfig(level=logging.INFO)

# URL des microservices
MICROSERVICE_STOCKS = "http://127.0.0.1:5001"
MICROSERVICE_EMPRUNTS = "http://127.0.0.1:5002"
MICROSERVICE_RETOURS = "http://127.0.0.1:5003"


@app.route('/action', methods=['POST'])
def effectuer_action():
    """
    Gère les différentes actions à envoyer vers les microservices :
    - Vérification du stock
    - Emprunt d'un livre
    - Retour d'un livre
    - Ajout de nouveau stock dans la bibliothèque
    """
    # Lecture des données envoyées par le client
    data = request.json
    action = data.get("action")
    id_livre = data.get("id_livre")
    utilisateur = data.get("utilisateur", "anonyme")  # Par défaut "anonyme"

    if not action or not id_livre:
        return jsonify({"message": "Les champs 'action' et 'id_livre' sont obligatoires."}), 400

    try:
        if action == "stock":
            # Vérification du stock
            response = requests.get(f"{MICROSERVICE_STOCKS}/livres/{id_livre}")
            if response.status_code == 200:
                return jsonify(response.json())
            return jsonify({"message": "Livre introuvable ou erreur du microservice Stocks."}), response.status_code

        elif action == "emprunt":
            # Emprunter un livre
            stock_response = requests.post(f"{MICROSERVICE_STOCKS}/livres/emprunt", json={"isbn": id_livre})
            if stock_response.status_code == 200:
                # S'il reste du stock, enregistrer l'emprunt
                emprunt_response = requests.post(
                    f"{MICROSERVICE_EMPRUNTS}/emprunt",
                    json={"id_livre": id_livre, "utilisateur": utilisateur}
                )
                return jsonify(emprunt_response.json()), emprunt_response.status_code
            else:
                return jsonify({"message": "Impossible d'emprunter, livre non disponible."}), 400

        elif action == "retour":
            # Retourner un livre
            retour_response = requests.post(f"{MICROSERVICE_STOCKS}/livres/retour", json={"isbn": id_livre})
            if retour_response.status_code == 200:
                # Enregistrer le retour dans le microservice retours
                retour_data = {"id_livre": id_livre, "utilisateur": utilisateur}
                requests.post(f"{MICROSERVICE_RETOURS}/retour", json=retour_data)
                return jsonify({"message": f"Livre {id_livre} retourné avec succès."})
            else:
                return jsonify({"message": "Erreur lors du retour, livre introuvable."}), 404

        elif action == "ajouter":
            # Ajouter un ou plusieurs livres dans le stock
            quantite = data.get("quantite", 1)

            payload_microservice = {
                "isbn": id_livre,  # Assurez-vous que 'isbn' est attendu côté microservice
                "titre": data.get("titre"),
                "auteur": data.get("auteur"),
                "annee": data.get("annee"),
                "stock": quantite
            }

            # LOGGING : Ajoutons un log pour voir ce qui est envoyé
            logging.info(f"Payload envoyé au microservice Stocks (ajouter_modifier_livre) : {payload_microservice}")

            ajouter_response = requests.post(
                f"{MICROSERVICE_STOCKS}/livres",
                json=payload_microservice
            )
            return jsonify(ajouter_response.json()), ajouter_response.status_code


        else:
            return jsonify({"message": "Action non reconnue. Veuillez vérifier vos paramètres."}), 400

    except requests.exceptions.ConnectionError as e:
        logging.error(f"Erreur de connexion lors de la communication avec un microservice : {e}")
        return jsonify({"message": "Erreur de connexion au microservice. Veuillez vérifier l'état des services."}), 500

    except Exception as e:
        logging.error(f"Erreur inattendue : {e}")
        return jsonify({"message": "Une erreur inattendue est survenue."}), 500


if __name__ == '__main__':
    app.run(port=5000)  # API Gateway sur le port 5000