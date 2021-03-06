from db import db

class RoleModel(db.Model):

    __tablename__='roles'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

    users = db.relationship('UserModel',lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name':self.name, 'users':[user.json() for user in self.users.all()]}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
