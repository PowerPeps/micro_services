import pymysql
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


# Connexion à MySQL avec gestion d’erreurs
def get_db_connection():
    try:
        return pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='bibliotheque',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        logging.error(f"Erreur de connexion à la base de données: {e}")
        raise


@app.route('/livres/<isbn>', methods=['GET'])
def verifier_stock(isbn):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM livres WHERE isbn = %s", (isbn,))
            livre = cursor.fetchone()
        if livre:
            return jsonify(livre)
        else:
            return jsonify({"message": "Livre introuvable"}), 404
    except Exception as e:
        logging.error(f"Erreur lors de la vérification du livre : {e}")
        return jsonify({"message": "Erreur interne du serveur."}), 500
    finally:
        connection.close()


@app.route('/livres', methods=['POST'])
def ajouter_modifier_livre():
    data = request.json
    isbn = data.get("isbn")
    titre = data.get("titre")
    auteur = data.get("auteur")
    annee = data.get("annee")
    stock = data.get("stock", 0)

    if not isbn or not titre or not auteur or not annee:
        return jsonify({"message": "Les champs ISBN, titre, auteur et année sont obligatoires."}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM livres WHERE isbn = %s", (isbn,))
            livre_existe = cursor.fetchone()

            if livre_existe:
                cursor.execute("UPDATE livres SET stock = stock + %s WHERE isbn = %s", (stock, isbn))
                message = f"Stock mis à jour pour le livre ISBN {isbn}."
            else:
                cursor.execute(
                    "INSERT INTO livres (isbn, titre, auteur, annee, stock) VALUES (%s, %s, %s, %s, %s)",
                    (isbn, titre, auteur, annee, stock)
                )
                message = f"Livre ajouté avec succès : '{titre}' par {auteur}."

        connection.commit()
        return jsonify({"message": message})
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout ou la modification d'un livre : {e}")
        return jsonify({"message": "Erreur interne du serveur."}), 500
    finally:
        connection.close()


@app.route('/livres/emprunt', methods=['POST'])
def emprunter_livre():
    data = request.json
    isbn = data.get("isbn")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT stock FROM livres WHERE isbn = %s", (isbn,))
            livre = cursor.fetchone()
            if livre and livre["stock"] > 0:
                cursor.execute("UPDATE livres SET stock = stock - 1 WHERE isbn = %s AND stock > 0", (isbn,))
                connection.commit()
                return jsonify({"message": f"Livre {isbn} emprunté avec succès."})
            else:
                return jsonify({"message": "Livre non disponible"}), 400
    except Exception as e:
        logging.error(f"Erreur lors de l'emprunt du livre : {e}")
        return jsonify({"message": "Erreur interne du serveur."}), 500
    finally:
        connection.close()


@app.route('/livres/retour', methods=['POST'])
def retourner_livre():
    data = request.json
    isbn = data.get("isbn")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM livres WHERE isbn = %s", (isbn,))
            livre = cursor.fetchone()
            if livre:
                cursor.execute("UPDATE livres SET stock = stock + 1 WHERE isbn = %s", (isbn,))
                connection.commit()
                return jsonify({"message": f"Livre {isbn} retourné avec succès."})
            else:
                return jsonify({"message": "Livre introuvable"}), 404
    except Exception as e:
        logging.error(f"Erreur lors du retour du livre : {e}")
        return jsonify({"message": "Erreur interne du serveur."}), 500
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(port=5001)