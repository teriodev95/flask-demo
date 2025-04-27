from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from faker import Faker
import random
import pycountry

app = Flask(__name__)

# Configuración de la base de datos SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'countries.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo Country
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    continent = db.Column(db.String(50), nullable=False)
    flag = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Country {self.name}>'

# Función para crear un país aleatorio
def create_random_country():
    fake = Faker()
    
    # Obtiene un país real de pycountry
    country = random.choice(list(pycountry.countries))
    
    # Nombre del país
    country_name = country.name
    
    # Intenta deducir continente (sólo una simulación, puedes mejorar con una librería como 'pycountry_convert')
    continents = ["América", "Europa", "Asia", "África", "Oceanía"]
    continent = random.choice(continents)
    
    # Extrae el emoji de bandera basado en el código alfa-2
    if hasattr(country, 'alpha_2'):
        flag = ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in country.alpha_2)
    else:
        flag = "🏳️"  # bandera blanca como fallback
    
    return Country(name=country_name, continent=continent, flag=flag)

# Rutas
@app.route('/', methods=['GET', 'POST'])
def index():
    # Si la solicitud es POST, procesamos el formulario
    if request.method == 'POST':
        name = request.form.get('name')
        continent = request.form.get('continent')
        flag = request.form.get('flag')
        
        # Crear nuevo país
        new_country = Country(name=name, continent=continent, flag=flag)
        db.session.add(new_country)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    # Obtener todos los países
    countries = Country.query.all()
    return render_template('index.html', countries=countries)

@app.route('/delete/<int:id>')
def delete(id):
    # Encontrar el país por ID
    country = Country.query.get_or_404(id)
    
    # Eliminarlo
    db.session.delete(country)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/create-random')
def create_random():
    # Crear un país aleatorio
    random_country = create_random_country()
    db.session.add(random_country)
    db.session.commit()
    
    return redirect(url_for('index'))

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 