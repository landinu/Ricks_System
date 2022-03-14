from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.role import RoleModel

class Role(Resource):

    @jwt_required()
    def get(self,name):
        role = RoleModel.find_by_name(name)
        if role:
            return role.json()
        return {'message':'Role not found'},404

    @jwt_required()
    def delete(self,name):
        role = RoleModel.find_by_name(name)
        if role:
            role.delete_from_db()
            return {'message':'Role deleted successfully'.format(role.name)},201
        return {'message':'Role not found'},404

    @jwt_required()
    def post(self,name):
        if RoleModel.find_by_name(name):
            return {"message":"Role already exists."},400
        role = RoleModel(name)
        role.save_to_db()
        return {"message":"Role created sucessfully."},201

class RoleList(Resource):
    @jwt_required()
    def get(self):
        return {'roles':[role.json() for role in RoleModel.query.all()]}

