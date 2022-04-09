from flask_restx import Namespace, Resource, fields
from flask import request,jsonify
from models import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token


auth_ns = Namespace('auth',description='A namespace for authentication')

signup_model = auth_ns.model('Signup',{
    "username":fields.String(),
    "email":fields.String(),
    "password":fields.String()
})


login_model = auth_ns.model('Login',{
    "username":fields.String(),
    "password":fields.String()
})


@auth_ns.route("/signup")
class SignUpResource(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        print(user)
        if user:
            return jsonify({'error':f"Username {username} Already Taken"},401)

        new_user = User(
            username = username,
            email = data.get('email'),
            password = generate_password_hash(password)
        )
        new_user.save()
        return jsonify({'msg':'User created successfully!!!'},201)

@auth_ns.route("/login")
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # filter user from db
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            return jsonify(
                {'acess_token':access_token,'refresh_token':refresh_token}
            )
        else:
            return jsonify({'error':"Invalid Credentials"})