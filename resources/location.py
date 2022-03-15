from flask_restful import Resource,reqparse
from flask_jwt import jwt_required, current_identity
from models.location import LocationModel
from models.user import UserModel
from models.multiverse import MultiverseModel

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
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1:
            location = LocationModel.find_by_name(name)
            if location:
                location.delete_from_db()
                return {'message':'Location {} was deleted'.format(location.name)}
            else:
                return {'message':'Location not found'},404
        else:
            return {'message':'Operation Unauthorized'},404

    @jwt_required()
    def put(self,name):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1:
            data = Location.parser.parse_args()
            location = LocationModel.find_by_name(name)
            if location:
                # Identificar si es un campo válido
                if data['field'] == 'multiverse':
                    multiverse = MultiverseModel.find_by_name(data['value'])
                    if multiverse:
                        location.multiverse_id = multiverse.id
                        location.save_to_db()
                        return {"message":"Location updated sucessfully."},201
                    else:
                        return {'message':'Multiverse not found'},404
                elif data['field'] == 'discover_date':
                    location.discover_date = data['value']
                    location.save_to_db()
                    return {"message":"Location updated sucessfully."},201
                elif data['field'] == 'last_visit':
                    location.last_visit = data['value']
                    location.save_to_db()
                    return {"message":"Location updated sucessfully."},201
                elif data['field'] == 'danger':
                    location.danger = int(data['value'])
                    location.save_to_db()
                    return {"message":"Location updated sucessfully."},201
                else:
                    return {'message':'Invalid field'},404
            else:
                return {'message':'Location not found'},404
        else:
            return {'message':'Operation Unauthorized'},404

    @jwt_required()
    def post(self,name):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1 or client.role_id == 2:
            data = Location.parser.parse_args()
            if LocationModel.find_by_name(name):
                return {"message":"Location already exists."},400
            # Obtener id del multiverso correspondiente y validar que exista
            multiverse = MultiverseModel.find_by_name(data['value'])
            if multiverse:
                location = LocationModel(name,multiverse.id)
                location.save_to_db()
                return {"message":"Location created sucessfully."},201
            else:
                return {'message':'Multiverse not found'},404
        else:
            return {'message':'Operation Unauthorized'},404

class LocationList(Resource):
    @jwt_required()
    def get(self):
        return {'locations':[location.json() for location in LocationModel.query.all()]}

