from db import db

class CharacterModel(db.Model):

    __tablename__='characters'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    first_meet = db.Column(db.String(20))
    last_meet = db.Column(db.String(20))
    ocupation = db.Column(db.String(80))
    location_id = db.Column(db.Integer,db.ForeignKey('locations.id'))

    def __init__(self, name,location_id):
        self.name = name
        self.location_id = location_id
        self.first_meet = None
        self.last_meet = None
        self.ocupation = None

    def json(self):
        return {'name':self.name, 'location_id':self.location_id, 'first_meet':self.first_meet,'last_meet':self.last_meet,'ocupation':self.ocupation}

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

