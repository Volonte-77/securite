#import de la bibliotheque mysql.connector
import mysql.connector
from cryptography.fernet import Fernet
import os

#on se connecte a la base de donnees mysql
def connect():
    bd = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="python"
        )
    return bd
#creation d'un curseur pour executer les requetes sql
curseur = connect().cursor()
#fonnction pour dechiffrees les donnees deja chiffrees dispo dans la bdd
def dechiffrer_message(message_chiffre):
    #recuperation de la cle a partir du variable d'environnement que j'ai nommee fernet
    cle=os.environ.get("fernet")
    if cle is None:
        raise ValueError("The 'fernet' environment variable is not set. Please set it before running this script.")
    #on charge le chiffrement
    chiffrement=Fernet(cle.encode())
    #dechiffrement du message
    message_dechiffre = chiffrement.decrypt(message_chiffre).decode()
    return message_dechiffre

#recuperation et affichage des donnees de la base de donnees
def afficher_utilisateurs():
    bd = connect()
    curseur = bd.cursor()
    requete = "SELECT email, nom, postnom FROM utilisateur"
    curseur.execute(requete)
    utilisateurs = curseur.fetchall()
    for utilisateur in utilisateurs:
        email_dechiffre = dechiffrer_message(utilisateur[0])
        nom_dechiffre = dechiffrer_message(utilisateur[1])
        postnom_dechiffre = dechiffrer_message(utilisateur[2])
        print(f"Email: {email_dechiffre}, Nom: {nom_dechiffre}, Postnom: {postnom_dechiffre}")
    curseur.close()
    bd.close()

afficher_utilisateurs()