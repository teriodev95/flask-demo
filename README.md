# Gestor de Países

Una aplicación web simple desarrollada con Flask que permite gestionar un catálogo de países. 

## Características

- Listado de países con su bandera, nombre y continente
- Formulario para agregar nuevos países
- Opción para eliminar países
- Interfaz de usuario estilo Uber con TailwindCSS

## Requisitos

- Python 3.6 o superior
- Flask
- Flask-SQLAlchemy
- Docker (opcional)

## Instalación

### Opción 1: Instalación local

1. Clona este repositorio o descarga los archivos.

2. Crea un entorno virtual (opcional pero recomendado):

   **MacOS/Linux**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Opción 2: Usando Docker

1. Clona este repositorio o descarga los archivos.

2. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.

## Ejecución

### Ejecución local

Para iniciar la aplicación:

**MacOS/Linux**:
```bash
python3 app.py
```

**Windows**:
```bash
python app.py
```

La aplicación estará disponible en la dirección http://127.0.0.1:5000/

### Ejecución con Docker

Para iniciar la aplicación con Docker:

```bash
docker-compose up
```

Para ejecutar en segundo plano:

```bash
docker-compose up -d
```

Para detener la aplicación:

```bash
docker-compose down
```

La aplicación estará disponible en la dirección http://localhost:5001/ 