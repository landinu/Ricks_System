from flask_restful import Resource,reqparse
from flask_jwt import jwt_required,current_identity
from models.user import UserModel
from models.role import RoleModel

class User(Resource):

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
        user = UserModel.find_by_name(name)
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if user and client.role_id == 1:
            return user.json()
        elif user and client.role_id != 1:
            return {'message':'Operation Unauthorized'},404
        return {'message':'User not found'},404

    @jwt_required()
    def delete(self,name):
        user = UserModel.find_by_name(name)
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if user and client.role_id == 1:
            user.delete_from_db()
            return {'message':'User {} was deleted'.format(user.username)}
        elif user and client.role_id != 1:
            return {'message':'Operation Unauthorized'},404
        return {'message':'User not found'},404

    @jwt_required()
    def put(self,name):
        data = User.parser.parse_args()
        # Se obtiene el rol del usuario loggeado
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        user = UserModel.find_by_name(name)
        if user and client.role_id == 1:
            if data['field'] == 'password':
                user.password = data['value']
                user.save_to_db()
                return {'message':'User updated successfully'},201
            elif data['field'] == 'role':
                role = RoleModel.find_by_name(data['value'])
                if role:
                    user.role_id = role.id
                    user.save_to_db()
                    return {'message':'User updated successfully'},201
                else:
                    return {'message':'Unknow role.'},404
            else:
                return {'message':'Invalid field'},404
        elif user and client.role_id != 1:
            return {'message':'Operation Unauthorized'},404
        return {'message':'User not found'},404

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument( 'username',
            type=str,
            required=True,
            help="This field cannot be blank."
    )
    parser.add_argument( 'password',
            type=str,
            required=True,
            help="This field cannot be blank."
    )
    parser.add_argument( 'role',
            type=str,
            required=True,
            help="This field cannot be blank."
    )

    @jwt_required()
    def post(self):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1:
            data = UserRegister.parser.parse_args()
            if UserModel.find_by_name(data['username']):
                return {"message":"User already exists."},400
            role = RoleModel.find_by_name(data['role'])
            user = UserModel(data['username'],data['password'],role.id)
            user.save_to_db()
            return {"message":"User created sucessfully."},201
        else:
            return {'message':'Operation Unauthorized'},404

class UserList(Resource):
    @jwt_required()
    def get(self):
        client = str(current_identity).replace('>','')
        client = client.split()
        client = UserModel.find_by_id(int(client[1]))
        if client.role_id == 1:
            return {'users':[user.json() for user in UserModel.query.all()]}
        else:
            return {'message':'Operation Unauthorized'},404

