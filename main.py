from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

from client import Client

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://172.18.0.35:27017/DBerick"
mongo = PyMongo(app)


# clients = [
#     Client(name="Zezinho", email="zezinho@univille.br", phone="11112222"),
#     Client(name="Pedrinho", email="pedrinho@univille.br", phone="11113333"),
#     Client(name="Joaquina", email="joaquina@univille.br", phone="11114444"),
#     Client(name="Zezinha", email="zezinha@univille.br", phone="11115555"),
#     Client(name="Paulinha", email="paulinha@univille.br", phone="11116666")
# ]


@app.route('/api/v1.0/clients', methods=['GET'])
def get_tasks():
    clients = []
    for c in mongo.db.clients.find():
        new_client = Client()
        new_client._id = str(c['_id'])
        new_client.name = c['name']
        new_client.phone = c['phone']
        new_client.email = c['email']
        clients.append(new_client)
    return jsonify([c.__dict__ for c in clients]), 201


@app.route('/api/v1.0/clients', methods=['POST'])
def create_client():
    # return jsonify({'clients': [client.__dict__ for client in clients]})
    new_client = Client()
    new_client._id = ObjectId()
    new_client.name = request.json['name']
    new_client.email = request.json['email']
    new_client.phone = request.json['phone']
    ret = mongo.db.clients.insert_one(new_client.__dict__).inserted_id
    return jsonify({'id': str(ret)}), 201


@app.route('/api/v1.0/clients/<string:_id>', methods=['PUT'])
def update_client(_id):
    updated_client = Client()
    updated_client._id = ObjectId(_id)
    updated_client.name = request.json['name']
    updated_client.email = request.json['email']
    updated_client.phone = request.json['phone']
    mongo.db.clients.update_one({'_id': updated_client._id},
                                      {"$set": updated_client.__dict__},
                                      upsert=False)
    return jsonify({'id': str(updated_client._id)}), 201

@app.route('/api/v1.0/clients/<string:_id>', methods=['DELETE'])
def delete_client(_id):
    _id = ObjectId(_id)
    returned = mongo.db.clients.delete_one({'_id': _id}).deleted_count
    return jsonify({'deleted_count': str(returned)}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
