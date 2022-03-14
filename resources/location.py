from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.location import LocationModel

class Location(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument( 'field',
            type=str,
            required=True,
            help="A field is necessary."
    )
    parser.add_argument( 'value',
            type=str,
            required=True,
            help="A value must be specified."
    )

    @jwt_required()
    def get(self,name):
        location = LocationModel.find_by_name(name)
        if location:
            return location.json()
        return {'message':'Location not found'},404

    @jwt_required()
    def delete(self,name):
        location = LocationModel.find_by_name(name)
        if location:
            location.delete_from_db()
            return {'message':'Location {} was deleted'.format(location.name)}
        return {'message':'Location not found'},404

    @jwt_required()
    def put(self,name):
        data = Location.parser.parse_args()
        client = get_jwt_identity()
        print (client)
        location = LocationModel.find_by_name(name)
        # Falta validar privilegios usuario
        if location:
            #user = UserModel(name,**data)
            # Identificar si es un campo válido
            if data['field'] == 'multiverse':
                location.multiverse_id = data['value']
            elif data['field'] == 'discover_date':
                location.discover_date = data['value']
            elif data['field'] == 'last_visit':
                location.last_visit = data['value']
            elif data['field'] == 'danger':
                location.danger = data['value']
            else:
                return {'message':'Invalid field'},404
        return {'message':'Location not found'},404

    @jwt_required()
    def post(self,name):
        data = Location.parser.parse_args()
        if LocationModel.find_by_name(name):
            return {"message":"Location already exists."},400
        # Obtener id del multiverso correspondiente y validar que exista
        location = LocationModel(**data)
        location.save_to_db()
        return {"message":"User created sucessfully."},201

class LocationList(Resource):
    @jwt_required()
    def get(self):
        return {'locations':[location.json() for location in LocationModel.query.all()]}

