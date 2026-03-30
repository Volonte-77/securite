#import de la bibliotheque mysql.connector
import mysql.connector
from cryptography.fernet import Fernet

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




#fonction pour inserer un utilisateur dans la base de donnees
def insererUtilisateur(email, nom, postnom):
    pass
