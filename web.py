from flask import Flask, render_template as template, request, redirect, url_for

# creation d'une instance de l'application Flask
application = Flask(__name__)

# stockage temporaire en mémoire (pour démonstration)
etudiants = []

# definition des routes et des fonctions associées
@application.route('/')
def home():
    return template('index.html')

@application.route('/enregistrer', methods=['GET', 'POST'])
def enregistrement():
    message = None
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        postnom = request.form.get('postnom', '').strip()
        email = request.form.get('email', '').strip()

        if not nom or not postnom or not email:
            message = "Tous les champs sont requis."
        else:
            etudiants.append({'nom': nom, 'postnom': postnom, 'email': email})
            message = f"Étudiant {nom} {postnom} ajouté avec succès."
            return redirect(url_for('liste_etudiants'))

    return template('form_etudiant.html', message=message)

@application.route('/liste')
def liste_etudiants():
    return template('liste.html', etudiants=etudiants)

# lancement de notre application
if __name__ == '__main__':
    application.run(debug=True)

