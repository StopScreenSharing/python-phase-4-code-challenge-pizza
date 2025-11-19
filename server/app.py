#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [r.to_dict(only=("address", "id", "name")) for r in restaurants], 200
    
class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id = id).first()
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        return restaurant.to_dict(), 200
    
    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        
        db.session.delete(restaurant)
        db.session.commit()

        return "", 204




@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantById, '/restaurants/<int:id>')


if __name__ == "__main__":
    app.run(port=5555, debug=True)
