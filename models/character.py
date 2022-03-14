from db import db

class CharacterModel(db.Model):

    __tablename__='characters'

    # Todos los atributos de la clase ItemModel deben estar definidos
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    location_id = db.Column(db.Integer,db.ForeignKey('location.id'))
    current_location_id = db.Column(db.Integer,db.ForeignKey('location.id'))
    firs_meet = db.Column(db.DateTime)
    last_meet = db.Column(db.DateTime)
    ocupation = db.Column(db.String(80))

    def __init__(self, name,location_id):
        self.name = name
        selff.location_id = location_id

    def json(self):
        return {'name':self.name, 'location_id':self.location_id}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

