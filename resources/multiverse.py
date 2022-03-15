from flask_restful import Resource,reqparse
from flask_jwt import jwt_required, current_identity
from models.multiverse import MultiverseModel
from models.user import UserModel

class Multiverse(Resource):

    @jwt_required()
    def get(self,name):
        multiverse = MultiverseModel.find_by_name(name)
        if multiverse:
            return multiverse.json()
        return {'message':'Multiverse not found'},404

    @jwt_required()
    def delete(self,name):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1:
            multiverse = MultiverseModel.find_by_name(name)
            if multiverse:
                multiverse.delete_from_db()
                return {'message':'Multiverse {} was deleted'.format(multiverse.name)}
            return {'message':'Multiverse not found'},404
        else:
            return {'message':'Operation Unauthorized'},404

    @jwt_required()
    def post(self,name):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1 or client.role_id == 2:
            if MultiverseModel.find_by_name(name):
                return {"message":"Multiverse already exists."},400
            multiverse = MultiverseModel(name)
            multiverse.save_to_db()
            return {"message":"Multiverse created sucessfully."},201
        else:
            return {'message':'Operation Unauthorized'},404

class MultiverseList(Resource):
    @jwt_required()
    def get(self):
        return {'multiverses':[multiverse.json() for multiverse in MultiverseModel.query.all()]}

