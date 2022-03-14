from hmac import compare_digest
from models.user import UserModel

def authenticate (username,password):
    user = UserModel.find_by_name(username) 
    if user and compare_digest(user.password, password): # Modo seguro de comparar cadenas, dadas las diferentes codificaciones.
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
