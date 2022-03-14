#
#   SOLUCIÓN BACKEND - RYCKS SYSTEM
#   
#   Archivo: app.py
#   Autor: Uri Landín
#   Fecha: 13 de marzo de 2022
#   Descripción: Sistema para almacenar
#   información de multiversos y personajes

# BIBLIOTECAS

import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# RECURSOS

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store, StoreList

# DESARROLLO APLICACIÓN

app = Flask(__name__)

# - Conexión con la base de datos

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL','sqlite:///data.db') # La variable JAWSDB_URL almacena el enlace a la base de datos que crea Heroku, en caso de que no este definida (prueba local) se utilizará la URL local (archivo data.db).
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Se deshabilita para optimizar el uso de memoria
app.secret_key = 'secret' # Acceso al diccionario de sesión 
api = Api(app) 

jwt = JWT(app,authenticate,identity) # Crea endpoint /auth para la autenticación se espera un usuario y un password

# - Declaración de recursos - Endpoints => http://domain/

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')

if __name__ == '__main__':
    app.run(port=5000, debug=True) # debug = True -> Arroja mensajes de error útiles para identificar el problema

