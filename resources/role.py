from flask_restful import Resource,reqparse
from flask_jwt import jwt_required, current_identity
from models.role import RoleModel
from models.user import UserModel

class Role(Resource):

    @jwt_required()
    def get(self,name):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1:
            role = RoleModel.find_by_name(name)
            if role:
                return role.json()
            return {'message':'Role not found'},404
        else:
            return {'message':'Operation Unauthorized'},404

    @jwt_required()
    def delete(self,name):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1:
            role = RoleModel.find_by_name(name)
            if role:
                role.delete_from_db()
                return {'message':'Role deleted successfully'.format(role.name)},201
            return {'message':'Role not found'},404
        else:
            return {'message':'Operation Unauthorized'},404

    @jwt_required()
    def post(self,name):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1:
            if RoleModel.find_by_name(name):
                return {"message":"Role already exists."},400
            role = RoleModel(name)
            role.save_to_db()
            return {"message":"Role created sucessfully."},201
        else:
            return {'message':'Operation Unauthorized'},404

class RoleList(Resource):
    @jwt_required()
    def get(self):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1:
            return {'roles':[role.json() for role in RoleModel.query.all()]}
        else:
            return {'message':'Operation Unauthorized'},404

