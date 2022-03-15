from db import db

class LocationModel(db.Model):

    __tablename__='locations'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    discover_date = db.Column(db.String(20))
    last_visit = db.Column(db.String(20))
    danger = db.Column(db.Integer)

    multiverse_id = db.Column(db.Integer,db.ForeignKey('multiverses.id'))
    #multiverse = db.relationship('MultiverseModel')
    
    characters = db.relationship('CharacterModel',lazy='dynamic')

    def __init__(self, name, multiverse_id):
        self.name = name
        self.multiverse_id = multiverse_id
        self.discover_date = None
        self.last_visit = None
        self.danger = "Unknow"

    def json(self):
        return {'name':self.name, 'multiverse_id':self.multiverse_id,'characters':[character.json() for character in self.characters.all()],'discover_date':self.discover_date,'last_visit':self.last_visit,'danger':self.danger}

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

