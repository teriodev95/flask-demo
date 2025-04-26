# Aplicación de Países

Una aplicación web simple desarrollada con Flask para gestionar un registro de países.

## Funcionalidades

- Listar países con su bandera, nombre y continente
- Agregar nuevos países
- Eliminar países existentes

## Requisitos

- Python 3.7 o superior
- Flask
- Flask-SQLAlchemy

## Instalación

### MacOS

```bash
# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python3 app.py
```

### Windows

```bash
# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
```

## Uso

1. Abre tu navegador y ve a `http://127.0.0.1:5000/`
2. Utiliza el formulario para agregar nuevos países
3. Visualiza la lista de países y elimina los que desees

La aplicación creará automáticamente la base de datos SQLite cuando se ejecute por primera vez. 