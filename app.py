from flask import Flask, render_template, request, redirect, url_for, flash
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
app.secret_key = 'clave_secreta_para_flash_messages'

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
        
        # Añadir mensaje flash para creación
        flash(f'¡País {name} creado correctamente!', 'success')
        
        return redirect(url_for('index'))
    
    # Obtener todos los países
    countries = Country.query.all()
    return render_template('index.html', countries=countries)

@app.route('/delete/<int:id>')
def delete(id):
    # Encontrar el país por ID
    country = Country.query.get_or_404(id)
    
    # Guardar el nombre para el mensaje
    country_name = country.name
    
    # Eliminarlo
    db.session.delete(country)
    db.session.commit()
    
    # Añadir mensaje flash para eliminación
    flash(f'País {country_name} eliminado correctamente', 'success')
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    # Obtener el país por ID
    country = Country.query.get_or_404(id)
    
    # Obtener todos los países para mostrarlos en la página
    countries = Country.query.all()
    
    # Renderizar la plantilla con el país a editar
    return render_template('index.html', countries=countries, edit_country=country)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    # Obtener el país por ID
    country = Country.query.get_or_404(id)
    
    # Actualizar los datos
    country.name = request.form.get('name')
    country.continent = request.form.get('continent')
    country.flag = request.form.get('flag')
    
    # Guardar cambios
    db.session.commit()
    
    # Añadir mensaje flash
    flash(f'¡País {country.name} actualizado correctamente!', 'success')
    
    return redirect(url_for('index'))

@app.route('/create-random')
def create_random():
    # Crear un país aleatorio
    random_country = create_random_country()
    db.session.add(random_country)
    db.session.commit()
    
    # Añadir mensaje flash
    flash(f'¡País aleatorio {random_country.name} creado correctamente!', 'success')
    
    return redirect(url_for('index'))

@app.route('/api/edit/<int:id>', methods=['POST'])
def api_edit(id):
    # Obtener el país por ID
    country = Country.query.get_or_404(id)
    
    # Verificar si se enviaron datos
    if not request.is_json:
        return {"error": "Se requiere JSON"}, 400
    
    data = request.get_json()
    
    # Actualizar solo los campos proporcionados
    if 'name' in data:
        country.name = data['name']
    if 'continent' in data:
        country.continent = data['continent']
    if 'flag' in data:
        country.flag = data['flag']
    
    # Guardar cambios
    db.session.commit()
    
    # Devolver respuesta
    return {"message": f"País {country.name} actualizado correctamente", "country": {
        "id": country.id,
        "name": country.name,
        "continent": country.continent,
        "flag": country.flag
    }}, 200

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 