from db import db

class LocationModel(db.Model):

    __tablename__='locations'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    discover_date = db.Column(db.DateTime)
    last_visit = db.Column(db.DateTime)
    danger = db.Column(db.Integer)

    multiverse_id = db.Column(db.Integer,db.ForeignKey('multiverses.id'))
    #multiverse = db.relationship('MultiverseModel')
    
    #objects = db.relationship('ObjectModel')
    
    characters = db.relationship('CharacterModel')

    def __init__(self, name, multiverse_id):
        self.name = name
        self.multiverse_id = multiverse_id

    # multiverse : MultiverseModel.find_by_id(self.multiverse_id)
    def json(self):
        return {'name':self.name, 'multiverse_id':self.multiverse_id}

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

