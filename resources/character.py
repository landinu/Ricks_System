from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.character import CharacterModel

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
        character = CharacterModel.find_by_name(name)
        if character:
            character.delete_from_db()
            return {'message':'Character {} was deleted'.format(character.name)}
        return {'message':'Character not found'},404

    @jwt_required()
    def put(self,name):
        data = Character.parser.parse_args()
        client = get_jwt_identity()
        print (client)
        character = CharacterModel.find_by_name(name)
        # Falta validar privilegios usuario
        if character:
            #character = CharacterModel(name,**data)
            if data['field'] == 'location_id':
                character.location_id = data['value']
            elif data['field'] == 'current_location':
                character.current_location = data['value']
            elif data['field'] == 'first_meet':
                character.first_meet = data['value']
            elif data['field'] == 'last_meet':
                character.last_meet = data['value']
            elif data['field'] == 'ocupation':
                character.ocupation = data['value']
            else:
                return {'message':'Invalid field'},404    
        return {'message':'Character not found'},404

    @jwt_required()
    def post(self,name):
        data = Character.parser.parse_args()
        if CharacterModel.find_by_name(name):
            return {"message":"Character already exists."},400
        # Obtener id de la locacion
        character = CharacterModel(**data)
        character.save_to_db()
        return {"message":"Character created sucessfully."},201

class CharacterList(Resource):
    @jwt_required()
    def get(self):
        return {'characters':[character.json() for character in CharacterModel.query.all()]}

