from flask_restful import Resource,reqparse
from flask_jwt import jwt_required, current_identity
from models.character import CharacterModel
from models.user import UserModel
from models.location import LocationModel

class Character(Resource):

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
        character = CharacterModel.find_by_name(name)
        if character:
            return character.json()
        return {'message':'Character not found'},404

    @jwt_required()
    def delete(self,name):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1:
            character = CharacterModel.find_by_name(name)
            if character:
                character.delete_from_db()
                return {'message':'Character {} was deleted'.format(character.name)}
            return {'message':'Character not found'},404
        else:
            return {'message':'Operation Unauthorized'},404

    @jwt_required()
    def put(self,name):

        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        
        if client.role_id == 1:
            
            data = Character.parser.parse_args()
            character = CharacterModel.find_by_name(name)
            if character:
                if data['field'] == 'location':
                    location = LocationModel.find_by_name(data['value'])
                    if location:
                        character.location_id = location.id
                        character.save_to_db()
                        return {"message":"Character updated sucessfully."},201
                    else:
                        return {'message':'Location not found'},404
                elif data['field'] == 'current_location':
                    location = LocationModel.find_by_name(data['value'])
                    if location:
                        character.location_id = location.id
                        character.save_to_db()
                        return {"message":"Character updated sucessfully."},201
                    else:
                        return {'message':'Location not found'},404
                elif data['field'] == 'first_meet':
                    character.first_meet = data['value']
                    character.save_to_db()
                    return {"message":"Character updated sucessfully."},201
                elif data['field'] == 'last_meet':
                    character.last_meet = data['value']
                    character.save_to_db()
                    return {"message":"Character updated sucessfully."},201
                elif data['field'] == 'ocupation':
                    character.ocupation = data['value']
                    character.save_to_db()
                    return {"message":"Character updated sucessfully."},201
                else:
                    return {'message':'Invalid field'},404    
            return {'message':'Character not found'},404
        else:
            return {'message':'Operation Unauthorized'},404

    @jwt_required()
    def post(self,name):

        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        
        if client.role_id == 1 or client.role_id == 2:
            
            data = Character.parser.parse_args()
            if CharacterModel.find_by_name(name):
                return {"message":"Character already exists."},400
            location = LocationModel.find_by_name(data['value'])
            if location:
                character = CharacterModel(name,location.id)
                character.save_to_db()
                return {"message":"Character created sucessfully."},201
            else:
                return {'message':'Location not found'},404
        else:
            return {'message':'Operation Unauthorized'},404

class CharacterList(Resource):
    @jwt_required()
    def get(self):
        return {'characters':[character.json() for character in CharacterModel.query.all()]}

