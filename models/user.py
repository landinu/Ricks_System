# Este programa es en si una API que comunica otra parte de nuestro programa con la Base de Datos
from db import db

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id')) # default=lector
    #role = db.relationship('RoleModel')

    def __init__ (self, username, password, role_id):
        self.username = username
        self.password = password
        self.role_id = role_id
    
    def json(self):
        return {'name':self.username, 'role':self.role_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
