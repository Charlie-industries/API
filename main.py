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

sString: str = os.environ.get("SSTRING")
uDatabase: str = os.environ.get("UDATABASE")
iDatabase: str = os.environ.get("IDATABASE")
eString: str = os.get("ESTRING")


def connection(appi, database):
    connection = sString + database + eString

    appi.config["MONGO_URI"] = connection
    mongoDB_client = PyMongo(appi)
    db = mongoDB_client.db

    return db

@app.route("/user")
def home():
    db = connection(app,uDatabase)

    testQs = db.testQ.find()
    response = dumps(testQs)
    return Response(response, mimetype="application/json")

@app.route('/user/<id>')
def user(id):
    db = connection(app,uDatabase)

    user = db.testQ.find_one({'_id': ObjectId(id)})
    response = dumps(user)
    return Response(response, mimetype="application/json")

@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    db = connection(app,uDatabase)

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
   db = connection(app,uDatabase)

   _json = request.json
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
    db = connection(app,uDatabase)

    db.testQ.delete_one({'_id': ObjectId(id)})
    resp = jsonify('User deleted successfully!')
    resp.status_code = 200
    return resp

@app.route('/receipts')
def receiptsHome():
    db = connection(app,iDatabase)

    invoiceQs = db.invoiceQ.find()
    response = dumps(invoiceQs)
    return Response(response, mimetype="application/json")

@app.route('/receipt/<id>')
def receipt(id):
    db = connection(app,iDatabase)

    invoiceQs = db.invoiceQ.find_one({'_id': ObjectId(id)})
    response = dumps(invoiceQs)
    return Response(response, mimetype="application/json")

@app.post('/addI')
def add_receipt():
    db = connection(app,iDatabase)

    _json = request.json
    cashierName = request.json["cashierName"]
    company = request.json["company"]
    address = request.json["address"]
    date = request.json["date"]
    item = request.json["item"]
    subTotal = _json["subTotal"]
    tax = _json["tax"]
    total = _json["total"]
    state = _json["state"]
    invoice_data = {
        "cashierName": cashierName,
        "company": company,
        "address": address,
        "date": date,
        "item": item,
        "subTotal": subTotal,
        "tax": tax,
        "total": total,
        "state": state
    }
    
    if invoice_data:
        id = db.invoiceQ.insert_one(invoice_data)
        response = jsonify({
            "_id": str(id.inserted_id),
            "cashierName": cashierName,
            "company": company,
            "address": address,
            "date": date,
            "item": item,
            "subTotal": subTotal,
            "tax": tax,
            "total": total,
            "state": state
        })

        response.status_code = 201
        return response
    else:
       return not_found()
   
@app.route('/deleteReceipt/<id>', methods=['DELETE'])
def delete_receipt(id):
    db = connection(app,iDatabase)
    db.invoiceQ.delete_one({'_id': ObjectId(id)})
    
    resp = jsonify('Receipt deleted successfully!')
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
