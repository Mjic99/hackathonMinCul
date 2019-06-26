from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
import pyrebase

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

config = {
    "apiKey": "AIzaSyDP4mF8cACK3oI7mA1Gak2GRhmLnOkCn9Q",
    "authDomain": "pahis-d3f4b.firebaseapp.com",
    "databaseURL": "https://pahis-d3f4b.firebaseio.com",
    "projectId": "pahis-d3f4b",
    "storageBucket": "pahis-d3f4b.appspot.com",
    "messagingSenderId": "787235694874",
    "appId": "1:787235694874:web:49a81c663aea0e72",
    "serviceAccount": "fbkey.json"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
    try:
        user = auth.sign_in_with_email_and_password(request.form['email'], request.form['password'])
        return redirect(url_for('index'))
    except:
        flash('Datos incorrectos')
        return redirect(url_for('login_page'))

@app.route("/signup", methods=['GET'])
def signup_page():
    return render_template('signup.html')
    
@app.route("/signup", methods=['POST'])
def signup():
    try:
        user = auth.create_user_with_email_and_password(request.form['email'], request.form['password'])
        return redirect(url_for('index'))
    except:
        flash('Error al crear cuenta')
        return redirect(url_for('signup_page'))

@app.route("/index", methods=['GET'])
def index():
    categorias = db.child('categorias').get().each()
    return render_template('index.html', categorias=categorias)

@app.route("/estilo/moderno")
def estilo():
    return render_template('moderno.html')

@app.route("/autor/walter")
def autor():
    return render_template('autor.html')

@app.route("/obra/tauro")
def obra():
    return render_template('tauro.html')

@app.route("/obra/tauro/detail")
def obra_detail():
    return render_template('tauro_detail.html')

@app.route("/alerta")   
def alerta():
    return render_template('alerta.html')

@app.route("/mapa")
def mapa():
    return render_template('mapa.html')

@app.route('/obras', methods = ['GET'])
def api_obras():
    filtrados = []
    obras = db.child("inmueblesLima").get()
    for obra in obras.each():
        if 'LATITUD' in obra.val() and 'LONGITUD' in obra.val():
            filtrados.append(obra.val())
    
    resp = jsonify(filtrados)
    resp.status_code = 200

    return resp

@app.route('/search_api', methods = ['GET'])
def search_api():
    filtrados = []
    obras = db.child("inmueblesLima").get()
    for obra in obras.each():
        if 'LATITUD' in obra.val() and 'LONGITUD' in obra.val():
            filtrados.append(obra.val())
    
    resp = jsonify(filtrados)
    resp.status_code = 200

    return resp

@app.route("/search")
def search():
    categorias = db.child('categorias').get().each()
    return render_template('search.html', categorias=categorias)

"""
/index con filtros js (buscador principal)
/autor
/monumento (con pestañas bloqueadas)
/mapa con links a sitios
/search filtros, tipo bib ulima
/estilos
"""