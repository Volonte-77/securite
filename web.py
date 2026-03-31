from flask import Flask, render_template as template, request, redirect, url_for, flash, jsonify
import os
from exercie_mysql import insererUtilisateur, supprimerUtilisateur, modifierUtilisateur
from dechiffrement import get_utilisateurs, get_utilisateur_by_id
# creation d'une instance de l'application Flask
application = Flask(__name__)
application.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

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
            flash(message, 'error')
        else:
            insererUtilisateur(email, nom, postnom)
            flash(f"Étudiant {nom} {postnom} ajouté avec succès.", 'success')
            return redirect(url_for('liste_etudiants'))

    # GET: afficher formulaire vide
    return template('form_etudiant.html', message=message, etudiant=None, action_url=url_for('enregistrement'))


@application.route('/modifier/<int:user_id>', methods=['GET', 'POST'])
def modifier(user_id):
    message = None
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        postnom = request.form.get('postnom', '').strip()
        email = request.form.get('email', '').strip()
        if not nom or not postnom or not email:
            message = "Tous les champs sont requis."
            flash(message, 'error')
        else:
            modifierUtilisateur(user_id, email, nom, postnom)
            flash("Utilisateur mis à jour avec succès.", 'success')
            return redirect(url_for('liste_etudiants'))

    # GET: pré-remplir le formulaire
    etudiant = get_utilisateur_by_id(user_id)
    if not etudiant:
        return redirect(url_for('liste_etudiants'))
    return template('form_etudiant.html', etudiant=etudiant, action_url=url_for('modifier', user_id=user_id), message=message)


@application.route('/supprimer/<int:user_id>', methods=['POST'])
def supprimer(user_id):
    supprimerUtilisateur(user_id)
    flash("Utilisateur supprimé.", 'success')
    return redirect(url_for('liste_etudiants'))


@application.route('/api/utilisateur/<int:user_id>')
def api_utilisateur(user_id):
    user = get_utilisateur_by_id(user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(user)

@application.route('/liste')
def liste_etudiants():
    # récupérer les utilisateurs déchiffrés depuis la base
    q = request.args.get('q', '').strip()
    domain = request.args.get('domain', '').strip()
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    per_page = 8
    etudiants = get_utilisateurs()
    if q:
        qlow = q.lower()
        etudiants = [e for e in etudiants if qlow in (e.get('nom','').lower() + ' ' + e.get('postnom','').lower() + ' ' + e.get('email','').lower())]
    if domain:
        dlow = domain.lower()
        etudiants = [e for e in etudiants if e.get('email','').lower().endswith(dlow)]
    total = len(etudiants)
    start = (page - 1) * per_page
    end = start + per_page
    page_etudiants = etudiants[start:end]
    total_pages = max(1, (total + per_page - 1) // per_page)
    return template('liste.html', etudiants=page_etudiants, q=q, domain=domain, page=page, total_pages=total_pages, total=total)

# lancement de notre application
if __name__ == '__main__':
    application.run(debug=True)

