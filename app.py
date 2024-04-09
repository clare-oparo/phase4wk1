from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    restaurants = db.relationship('RestaurantPizza', back_populates='pizza')

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    restaurant = db.relationship('Restaurant', back_populates='pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurants')

    __table_args__ = (
        db.CheckConstraint('price >= 1 AND price <= 30', name='price_check'),
    )

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify({
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": [
                {"id": rp.pizza.id, "name": rp.pizza.name, "ingredients": rp.pizza.ingredients}
                for rp in restaurant.pizzas
            ]
        })
    else:
        return jsonify({"error": "Restaurant not found"}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"error": "Restaurant not found"}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'ingredients': p.ingredients} for p in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    try:
        restaurant_pizza = RestaurantPizza(price=data['price'], pizza_id=data['pizza_id'], restaurant_id=data['restaurant_id'])
        db.session.add(restaurant_pizza)
        db.session.commit()
        pizza = Pizza.query.get(restaurant_pizza.pizza_id)
        return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients})
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400


def seed_data():
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    dominion_pizza = Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue")
    pizza_hut = Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100")
    
    db.session.add(dominion_pizza)
    db.session.add(pizza_hut)
    
    db.session.commit()

    cheese_pizza = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni_pizza = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    
    db.session.add(cheese_pizza)
    db.session.add(pepperoni_pizza)

    db.session.commit()

    db.session.add(RestaurantPizza(price=10, restaurant_id=dominion_pizza.id, pizza_id=cheese_pizza.id))
    db.session.add(RestaurantPizza(price=12, restaurant_id=pizza_hut.id, pizza_id=pepperoni_pizza.id))

    db.session.commit()

@app.cli.command("seed_db")
def seed_db_command():
    """Seeds the database with initial data."""
    seed_data()
    print("Database seeded.")



