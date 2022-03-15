from app import app
from db import db
from models.user import UserModel
from models.role import RoleModel

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all() # Unicamente crea las tablas que ve (los archivos que se importan)
    
    role = RoleModel("admin")
    role.save_to_db()
    role = RoleModel("member")
    role.save_to_db()
    role = RoleModel("reader")
    role.save_to_db()

    user = UserModel("Rick","Rick123",1)
    user.save_to_db()
    user = UserModel("Morty","Morty123",2)
    user.save_to_db()
    user = UserModel("Summer","Summer123",3)
    user.save_to_db()
