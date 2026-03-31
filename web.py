from flask import Flask,render_template as template
#creation d'une instance de l'application Flask
application = Flask(__name__)

#definition des routes et des fonctions associées
@application.route('/')
def home():
    return template('index.html')

#lancement de notre application

if __name__ == '__main__':
    application.run(debug=True)
