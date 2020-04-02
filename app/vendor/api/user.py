from flask import jsonify, request
from flask_restplus import Api, Resource, Namespace, fields
from app.vendor.dao.user import UserDao
from app.vendor.models.user import User as UserModel
from app.vendor.exception import ApplicationException
from app.vendor.util.decorator import token_required


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.String(),
        'firstname': fields.String(required=True),
        'lastname': fields.String(required=True),
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'created_date': fields.DateTime(required=True),
        'last_login_date': fields.String(required=True)
    })

api = UserDto.api
_user = UserDto.user

get_parser = api.parser()
get_parser.add_argument('Authorization', location='headers')

@api.route("/")
@api.expect(get_parser)
class UserList(Resource):
    """
    This class contains the functions to run the API request.
    HTTP methods are implemented as functions.  Currently,
    this API only supports HTTP GET
    """

    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='userlist')
    @token_required
    def get(self):
        """Get all users"""
        try:
            users = UserDao.get_all()
            user_ret_list = []
            for user in users:
                user_ret_list.append(user.to_json())
            return user_ret_list
        except ApplicationException as e:
            error_message = str(e)
            return jsonify(error_message=error_message[:200])

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=False)
    @api.marshal_with(_user)
    @token_required
    def post(self):
        """Insert a user"""
        try:
            # ToDo: need to add logic to check if email and user already exist
            user_data = request.json
            new_user = UserModel()
            new_user.firstname = user_data['firstname']
            new_user.lastname = user_data['lastname']
            new_user.username = user_data['username']
            new_user.email = user_data['email']
            new_user.set_password(user_data['password'])
            new_user = UserDao.save_user(new_user)
            return new_user
        except ApplicationException as e:
            error_message = str(e)
            return jsonify(error_message=error_message[:200]) 


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):

    @api.doc('get a user')
    @api.marshal_with(_user)
    @api.expect(get_parser)
    @token_required
    def get(self, id):
        """Get a user given its identifier"""
        user = UserDao.get_by_id(id)
        if not user:
            api.abort(404)
        else:
            return user
