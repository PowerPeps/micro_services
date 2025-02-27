import requests
import json

# URL de l'API Gateway
API_GATEWAY_URL = "http://127.0.0.1:5000"


def effectuer_action(action, data):
    """
    Effectuer une requête POST vers l'API Gateway.
    """
    try:
        response = requests.post(f"{API_GATEWAY_URL}/action", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"message": f"Erreur : {response.status_code}, {response.text}"}
    except requests.exceptions.ConnectionError:
        return {"message": "Impossible de se connecter à l'API Gateway."}


def afficher_menu():
    """
    Affiche le menu principal pour l'utilisateur.
    """
    print("=" * 50)
    print("==\t\t BIBLIOTHÈQUE CENTRALE \t\t==")
    print("=" * 50)
    print("Choisir une action :")
    print("\t1 - Vérifier le stock d'un livre")
    print("\t2 - Emprunter un livre")
    print("\t3 - Retourner un livre")
    print("\t4 - Ajouter un livre dans le stock")
    print("\t5 - Quitter l'application\n")


def verifier_stock():
    """
    Vérifie la disponibilité d'un livre.
    """
    id_livre = input("Entrez l'identifiant du livre : ")
    réponse = effectuer_action("stock", {"action": "stock", "id_livre": id_livre})
    if "stock" in réponse:
        print(f"Stock disponible pour '{id_livre}': {réponse['stock']} exemplaire(s).")
    else:
        print(réponse.get("message", "Erreur inconnue lors de la vérification du stock."))


def emprunter_livre():
    """
    Emprunte un livre si disponible.
    """
    id_livre = input("Entrez le nom ou l'identifiant du livre à emprunter : ")
    utilisateur = input("Entrez votre nom ou votre identifiant utilisateur : ")
    # Vérifier si le stock est suffisant avant d'emprunter
    réponse_stock = effectuer_action("stock", {"action": "stock", "id_livre": id_livre})
    if réponse_stock.get("stock", 0) > 0:
        réponse_emprunt = effectuer_action("emprunt",
                                           {"action": "emprunt", "id_livre": id_livre, "utilisateur": utilisateur})
        print(réponse_emprunt.get("message", "Erreur lors de l'emprunt du livre."))
    else:
        print(f"Le livre '{id_livre}' n'est pas en stock.")


def retourner_livre():
    """
    Retourne un livre emprunté.
    """
    id_livre = input("Entrez le nom ou l'identifiant du livre à retourner : ")
    utilisateur = input("Entrez votre nom ou votre identifiant utilisateur : ")
    réponse = effectuer_action("retour", {"action": "retour", "id_livre": id_livre, "utilisateur": utilisateur})
    print(réponse.get("message", "Erreur lors du retour du livre."))


def ajouter_livre():
    isbn = input("Entrez l'ISBN du livre : ")
    titre = input("Entrez le titre du livre : ")
    auteur = input("Entrez l'auteur : ")
    annee = int(input("Entrez l'année de publication : "))
    quantite = int(input("Entrez la quantité : "))
    data = {"action": "ajouter", "isbn": isbn, "titre": titre, "auteur": auteur, "annee": annee, "stock": quantite}
    réponse = effectuer_action("ajouter", data)
    print(réponse.get("message", "Erreur lors de l'ajout du livre."))


def main():
    """
    Boucle principale pour afficher le menu et exécuter les actions choisies.
    """
    while True:
        afficher_menu()
        choix = input("Entrez votre choix : ")
        if choix == "1":
            verifier_stock()
        elif choix == "2":
            emprunter_livre()
        elif choix == "3":
            retourner_livre()
        elif choix == "4":
            ajouter_livre()
        elif choix == "5":
            print("Au revoir ! Merci d'avoir utilisé notre système.")
            break
        else:
            print("Choix invalide, veuillez réessayer.")


if __name__ == "__main__":
    main()
