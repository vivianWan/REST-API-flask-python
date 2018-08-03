from flask import Flask, jsonify, request

app1 = Flask(__name__)

stores = [ 
    { 
        "name": "My Wonderful Store", 
        "item":[
            {
                "name":"My Item", 
                "price":15.99
            }
        ]
    }
]

# POST - used to receive data
# GET - used to send data back only 

# POST /store data: {name:}
@app1.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app1.route('/store/<string:name>')    # 'thhp://127.0.0.1:500/store/some_name'
def get_store(name):
    # Iterate over stores
    # if the sotre name matches, returen it
    # if none match, return an error message
    for store in stores:
        if store['name'] == name:
            return (jsonity(store))
    return jsonify({'message': 'store not found'})

# GET /store
@app1.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:,price}
@app1.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)

    return jsonify({'message': 'store not found'})

# GET /store/<string:name>/item
@app1.route('/store/<string:name>/item')
def get_items_in_store(name):
    for sotre in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
        
    return jsonify ({'message': 'store not found'})

app1.run(port=5000)