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
from resources.user import User, UserRegister, UserList 
from resources.rol import Rol, RolRegister, RolList
from resources.location import Location, LocationRegister, LocationList
from resources.character import Character, CharacterRegister, CharacterList
#from resources.object import Object, ObjectRegister,ObjectList
from resources.multiverse import Multiverse, MultiverseRegister, MultiverseList

# DESARROLLO APLICACIÓN

app = Flask(__name__)

# - Conexión con la base de datos

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL','sqlite:///data.db') # La variable JAWSDB_URL almacena el enlace a la base de datos que crea Heroku, en caso de que no este definida (prueba local) se utilizará la URL local (archivo data.db).
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Se deshabilita para optimizar el uso de memoria
app.secret_key = 'secret' # Acceso al diccionario de sesión 
api = Api(app) 

jwt = JWT(app,authenticate,identity) # Crea endpoint /auth para la autenticación se espera un usuario y un password

# - Declaración de recursos - Endpoints => http://domain/

api.add_resource(User,'/user/<string:name>')
api.add_resource(UserRegister,'/register')
api.add_resource(UserList,'/users')
api.add_resource(Rol,'/role/<string:name>')
api.add_resource(RolRegister,'/new-role')
api.add_resource(RolList,'/roles')
api.add_resource(Location,'/location/<string:name>')
api.add_resource(LocationRegister,'/new-location')
api.add_resource(LocationList,'/locations')
api.add_resource(Character,'/character/<string:name>')
api.add_resource(CharacterRegister,'/new-character')
api.add_resource(CharacterList,'/characters')
#api.add_resource(Object,'/object/<string:name>')
#api.add_resource(ObjectRegister,'/new-object')
#api.add_resource(ObjectList,'/objects')
api.add_resource(Multiverse,'/multiverse/<string:name>')
api.add_resource(MultiverseRegister,'/new-multiverse')
api.add_resource(MultiverseList,'/multiverses')

if __name__ == '__main__':
    app.run(port=5000, debug=True) # debug = True -> Arroja mensajes de error útiles para identificar el problema

