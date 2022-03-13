from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all() # Unicamente crea las tablas que ve (los archivos que se importan)
