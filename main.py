from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask import Flask, Response
import os

load_dotenv()

app = Flask(__name__)
app.debug = True

connection_string: str = os.environ.get("CONNECTION_STRING")
connection_string = connection_string

if not connection_string:
    raise ValueError("MongoDB connection string not found in environment variables")

app.config["MONGO_URI"] = connection_string


mongoDB_client = PyMongo(app)
db = mongoDB_client.db

@app.route("/")
def root():
    return 'Hi'

@app.route("/user")
def home():
    testQs = db.testQ.find()
    response = dumps(testQs)
    return Response(response, mimetype="application/json")

@app.route('/user/<id>')
def user(id):
    user = db.testQ.find_one({'_id': ObjectId(id)})
    response = dumps(user)
    return Response(response, mimetype="application/json")

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _json = request.json

    _firstName = _json['firstName']
    _lastName = _json['lastName']
    _username = _json['username']
    _email = _json['email']
    _password = _json['password']
    _signUpDate = _json['signUpDate']

    
    if _firstName and _lastName and _username and _email and _password and _signUpDate and request.method == 'PUT':
        
        db.testQ.update_one({'_id': ObjectId(id)},
                            {'$set': {'firstName': _firstName,
                                      'lastName': _lastName,
                                      'username': _username,
                                      'email': _email,
                                      'password': _password,
                                      'signUpDate': _signUpDate}})
        
        resp = jsonify('User updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.post('/add')
def add_data():
   _json = request.json
   print("JSON ", _json)
   firstName = request.json["firstName"]
   lastName = request.json["lastName"]
   username = request.json["username"]
   email = request.json["email"]
   password = request.json["password"]
   signUpDate = request.json["signUpDate"]

   if username and email and password:
       
       id = db.testQ.insert_one({'firstName':firstName,
                                 'lastName':lastName,
                                 'username':username,
                                 'email':email,
                                 'password':password,
                                 'signUpDate':signUpDate})
       response = jsonify({
           "_id": str(id),
           "firstName":firstName,
           "lastName":lastName,
           "username":username,
           "email":email,
           "password":password,
           "signUpDate":signUpDate
       })

       response.status_code = 201
       return response
   else:
       return not_found()

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
	db.testQ.delete_one({'_id': ObjectId(id)})
	resp = jsonify('User deleted successfully!')
	resp.status_code = 200
	return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()
