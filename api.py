from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' 
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    def __repr__(self):
        return f"User('name = {self.name}', email = '{self.email}')"

user_args = reqparse.RequestParser()
user_args.add_argument('name', type = str, help = "Name of the user cannot be blanked", required = True)  
user_args.add_argument('email', type = str, help = "Email of the user cannot be blanked", required = True)  

userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

class User(Resource):
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name = args['name'], email = args['email'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201

    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, "User not found")
        return user
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id = id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id = id).first()
        user["name"] = args["name"]
        user["email"] = args["email"]
        db.session.commit()
        if not user:
            abort(404, "User not found")
        return user

api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:id>')

@app.route('/')
def index():
    return "<h1>This is FLASK</h1>"

if __name__ == "__main__":
    app.run(debug=True)