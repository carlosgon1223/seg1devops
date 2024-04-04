from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)

    def __init__(self, name):
        self.name = name

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id

class ClientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'client_id')

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@app.route('/client', methods=['POST'])
def add_client():
    name = request.json['name']

    new_client = Client(name)

    db.session.add(new_client)
    db.session.commit()

    return client_schema.jsonify(new_client)

@app.route('/client/<id>', methods=['GET'])
def get_client(id):
    client = Client.query.get(id)
    return client_schema.jsonify(client)

@app.route('/client', methods=['GET'])
def get_clients():
    all_clients = Client.query.all()
    result = clients_schema.dump(all_clients)
    return jsonify(result)

@app.route('/item', methods=['POST'])
def add_item():
    name = request.json['name']
    client_id = request.json['client_id']

    new_item = Item(name, client_id)

    db.session.add(new_item)
    db.session.commit()

    return item_schema.jsonify(new_item)

@app.route('/item/<id>', methods=['GET'])
def get_item(id):
    item = Item.query.get(id)
    return item_schema.jsonify(item)

@app.route('/item', methods=['GET'])
def get_items():
    all_items = Item.query.all()
    result = items_schema.dump(all_items)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)