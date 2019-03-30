import os

from flask import Flask
from flask import jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity as identity_function
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

# if in local not in Hero
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Turn off the Flask_SQLALchemy tracker but not SQLALchemy
app.secret_key = 'jerry' # This needs to be hidden in Production
api = Api(app)

jwt = JWT(app, authenticate, identity_function) # /auth

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                    'access_token': access_token.decode('utf-8'),
                    'user_id': identity.id
                    })

@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
                    'message': error.description,
                    'code': error.status_code
                   }), error.status_code

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
