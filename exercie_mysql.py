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


#fonnction pour chiffrer un message
def chiffrer_message(message_clair):
    #recuperation de la cle a partir du variable d'environnement que j'ai nommee fernet
    cle=os.environ.get("fernet")
    if cle is None:
        raise ValueError("The 'fernet' environment variable is not set. Please set it before running this script.")
    #on charge le chiffrement
    chiffrement=Fernet(cle.encode())
    #chiffrement du message
 
    message_chiffre = chiffrement.encrypt(message_clair.encode())
    return message_chiffre

#fonction pour inserer un utilisateur dans la base de donnees
"""def insererUtilisateur(email, nom, postnom):
    #chiffrement des informations sensibles
    email_chiffre = chiffrer_message(email)
    nom_chiffre = chiffrer_message(nom)
    postnom_chiffre = chiffrer_message(postnom)
    
    #insertion dans la base de donnees
    requete = "INSERT INTO utilisateurs (email, nom, postnom) VALUES (%s, %s, %s)"
    valeurs = (email_chiffre, nom_chiffre, postnom_chiffre)
    curseur.execute(requete, valeurs)
    connect().commit()"""
print(chiffrer_message("je vous salue"))