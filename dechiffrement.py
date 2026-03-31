#import de la bibliotheque mysql.connector
import mysql.connector
from cryptography.fernet import Fernet
import os


# Connexion à la base de données
def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python"
    )


def _get_fernet():
    cle = os.environ.get("fernet")
    if cle is None:
        raise ValueError("The 'fernet' environment variable is not set. Please set it before running this script.")
    return Fernet(cle.encode())


def dechiffrer_message(message_chiffre):
    """Déchiffre un champ (bytes ou str) et retourne une chaîne."""
    if message_chiffre is None:
        return ""
    if isinstance(message_chiffre, str):
        message_chiffre = message_chiffre.encode()
    chiffrement = _get_fernet()
    try:
        return chiffrement.decrypt(message_chiffre).decode()
    except Exception:
        # en cas d'erreur, retourner la valeur brute décodée si possible
        try:
            return message_chiffre.decode()
        except Exception:
            return ""


def get_utilisateurs():
    """Retourne une liste de dicts {'nom','postnom','email'} avec les valeurs déchiffrées."""
    resultat = []
    bd = connect()
    curseur = bd.cursor()
    requete = "SELECT id, email, nom, postnom FROM utilisateur"
    curseur.execute(requete)
    utilisateurs = curseur.fetchall()
    for utilisateur in utilisateurs:
        uid = utilisateur[0]
        email_dechiffre = dechiffrer_message(utilisateur[1])
        nom_dechiffre = dechiffrer_message(utilisateur[2])
        postnom_dechiffre = dechiffrer_message(utilisateur[3])
        resultat.append({
            'id': uid,
            'email': email_dechiffre,
            'nom': nom_dechiffre,
            'postnom': postnom_dechiffre
        })
    curseur.close()
    bd.close()
    return resultat


def get_utilisateur_by_id(user_id):
    """Retourne un dict pour un utilisateur par id (déchiffré), ou None."""
    bd = connect()
    curseur = bd.cursor()
    requete = "SELECT id, email, nom, postnom FROM utilisateur WHERE id = %s"
    curseur.execute(requete, (user_id,))
    row = curseur.fetchone()
    curseur.close()
    bd.close()
    if not row:
        return None
    uid = row[0]
    email_dechiffre = dechiffrer_message(row[1])
    nom_dechiffre = dechiffrer_message(row[2])
    postnom_dechiffre = dechiffrer_message(row[3])
    return {'id': uid, 'email': email_dechiffre, 'nom': nom_dechiffre, 'postnom': postnom_dechiffre}


def afficher_utilisateurs():
    """Compatibilité : affiche en console les utilisateurs (utilisé en script)."""
    for u in get_utilisateurs():
        print(f"Email: {u['email']}, Nom: {u['nom']}, Postnom: {u['postnom']}")


if __name__ == '__main__':
    afficher_utilisateurs()