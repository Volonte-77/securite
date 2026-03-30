from cryptography.fernet import Fernet

message_clair = b"Bonjour, ceci est un message secret!"

#generer une cle de chiffrement
cle_de_chiffrement = Fernet.generate_key()

#charger l'algorithme de chiffrement 
chiffrement=Fernet(cle_de_chiffrement)

#chiffrement du message
message_chiffre = chiffrement.encrypt(message_clair)
#dechiffrement
message_dechiffre = chiffrement.decrypt(message_chiffre)

print("Message clair:", message_clair)
print("Message chiffré:", message_chiffre)
#apres dechiffrement, le message est lisible
print("Message déchiffré:", message_dechiffre.decode())