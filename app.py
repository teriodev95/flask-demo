from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración para entorno de desarrollo y producción
if os.environ.get('VERCEL_ENVIRONMENT') == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///countries.db')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///countries.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    continent = db.Column(db.String(50), nullable=False)
    flag = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Country {self.name}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        continent = request.form['continent']
        flag = request.form['flag']
        
        new_country = Country(name=name, continent=continent, flag=flag)
        db.session.add(new_country)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    countries = Country.query.all()
    return render_template('index.html', countries=countries)

@app.route('/delete/<int:id>')
def delete(id):
    country = Country.query.get_or_404(id)
    db.session.delete(country)
    db.session.commit()
    return redirect(url_for('index'))

# Crear las tablas de la base de datos
with app.app_context():
    db.create_all()

# Para entorno de desarrollo local
if __name__ == '__main__':
    app.run(debug=True) 