from db import db

class ObjectModel(db.Model):

    __tablename__='objects'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    location_id = db.Column(db.Integer,db.ForeignKey('locations.id'))
    current_location = db.Column(db.Integer,db.ForeignKey('locations.id'))
    value = db.Column(db.Integer)
    interest = db.Column(db.String(150))

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name':self.name}

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

