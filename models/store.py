from db import db

class StoreModel(db.Model):

    __tablename__='stores'

    # Todos los atributos de la clase ItemModel deben estar definidos
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel',lazy='dynamic') # Esta es una lista porque es una relación 1:M
    # lazy = dynamic => Query builder que puede ver en la tabla de items. No crea objetos ItemModel
    # Ya que se tiene que consultar la tabla cada que se consulte una tienda, es más lento al llamar al método json(), pero la creación de la tienda será rápida.

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name':self.name, 'items':[item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

