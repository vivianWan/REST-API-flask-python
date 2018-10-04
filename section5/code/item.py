import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument ('price', 
        type = float,
        required = True,
        help ="This field cannot be left blank!"
    )

#    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400
        
        data = Item.parser.parse_args()

        item ={'name': name, 'price':data['price']}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item, 201

#    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE  items VALUES (?,?)"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)

        update_item = {'name': name, 'price':data['price']}
        if item is None:
            try: 
                Item.insert(update_item)
            except:
                return {'message': 'An error occurred inserting the item. '}
        else:
            try: 
                Item.update(update_item)
            except:
                return {'message':'An error occurred updating the item. '}
        return update_item

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()


    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "UPDATE items SET price =? WHERE name = ?"
        cursor.execute(query, (item['price'],item['name']))

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        items =[]

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items "
        result = cursor.execute(query)
        for row in result:
            items.append({'name':row[0], 'pricae':row[1]})
        connection.close()

        return {'items': items}