import time
from flask import *
import sys
import random
    
#NE PAS MODIFIER LA LIGNE SUIVANTE
app = Flask(__name__)



nb_dev = 0
encours = False
tour = 0

@app.route("/")
def index():
    error = request.args.get('error')
    return render_template("index.html", hasError=error)


@app.route('/jeu')
def deb_jeu():
    global nb_dev
    global tour
    error = request.args.get('error')

    min_ = int(request.args.get('min'))
    max_ = int(request.args.get('max'))
    essais = int(request.args.get('essais'))

    print(min_)
    print(max_)

    if min_ >= max_:
        return render_template("index.html" , hasError="Choisissez un intervalle correct !")
    if essais == 0:
        return render_template("index.html" , hasError="Choisissez un nombre d'essais correct !")


    try:
        number = int(request.args.get('number'))
    except:
        number = None
    
    if encours == False :
        nb_dev = random.randint(min_,max_)
    return render_template("jeu.html" , hasError=error, tour = tour, nb = nb_dev, number = number, min = min_, max=max_, essais=essais)


@app.route('/nombre')
def in_game():
    global nb_dev
    global encours
    encours = True
    try :
        number = int(request.args.get('nb'))
        min_ = int(request.args.get('min'))
        max_ = int(request.args.get('max'))
        essais = int(request.args.get('essais'))

    except:
        number = None
    global tour
    tour = tour + 1
    
    if number == nb_dev:
        return render_template("end.html", tour = tour, win = True, nb = nb_dev,  min = min_, max=max_, essais=essais)
    elif tour < essais:
        return redirect(url_for('deb_jeu', error="Vous n'avez pas encore trouvé, essayez encore!", number = number, min = min_, max=max_, essais=essais))
    else:
        return render_template("end.html",  tour = tour, win = False, nb = nb_dev,  min = min_, max=max_, essais=essais)
        
@app.route('/retenter')
def encore ():
    global encours
    encours = False
    global tour
    tour = 0

    min_ = int(request.args.get('min'))
    max_ = int(request.args.get('max'))
    essais = int(request.args.get('essais'))

    value = request.args.get('custId')

    if value == 'Recommencer':
        return redirect(url_for('deb_jeu', min = min_, max=max_, essais=essais))
    elif value == "Changer les Paramètres":
        return redirect(url_for('index'))


#NE SURTOUT PAS MODIFIER     
#CES DEUX LIGNES DOIVENT TOUJOURS ETRE LES DERNIERES
if __name__ == "__main__":
   app.run(debug=True, host='0.0.0.0', port='5000')
