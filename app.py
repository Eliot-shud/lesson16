import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import raw_data
from models import User, Order, Offer

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# views users
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        result = []
        for u in User.query.all():
            result.append(u.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )

        db.session.add(new_user)
        db.session.commit()

        return "User created", 201



@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def user(uid: int):

    if request.method == "GET":
        return json.dumps(User.guery.get(uid).to_dict()), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        u = User.query.get(uid)
        u.first_name = user_data["first_name"]
        u.last_name = user_data["last_name"]
        u.age = user_data["age"]
        u.email = user_data["email"]
        u.role = user_data["role"]
        u.phone = user_data["phone"]

        db.session.add(u)
        db.session.commit()

        return "User updated", 204

    if request.method == "DELETE":
        u = User.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "User deleted", 204


# views orders

@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        result = []
        for u in Order.query.all():
            result.append(u.to_dict())
        return json.dumps(result), 200

    if request.method == "POST":
        order_data = json.loads(request.data)
        new_order = User(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"],
        )

        db.session.add(new_order)
        db.session.commit()

        return "Order Created", 201

@app.route("/orders/<int:uid>", methods=["GET", "PUT", "DELETE"])
def order(uid: int):
    if request.method == "GET":
        return json.dumps(Order.guery.get(uid).to_dict()), 200
    if request.method == "POST":
        order_data = json.loads(request.data)
        u = User.query.get(uid)
        u.name = order_data["name"]
        u.description = order_data["description"]
        u.start_date = order_data["start_date"]
        u.end_date = order_data["end_date"]
        u.address = order_data["address"]
        u.price = order_data["price"]
        u.customer_id = order_data["customer_id"]
        u.executor_id = order_data["executor_id"]

        db.session.add(u)
        db.session.commit()

        return "Order updated", 204
    if request.method == "DELETE":
        u = Order.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Order Deleted", 204


# views offers
@app.route("/offers", methods=["GET", "POST"])
def offers():
    if request.method == "GET":
        result = []
        for u in Offer.query.all():
            result.append(u.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = User(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"],
        )

        db.session.add(new_offer)
        db.session.commit()

        return "Offer Created", 201


@app.route("/offers/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offers(uid: int):
    if request.method == "GET":
        return json.dumps(Offer.guery.get(uid).to_dict()), 200

    if request.method == "PUT":
        offer_data = json.loads(request.data)
        u = Offer.query.get(uid)
        u.order_id = offer_data["order_id"]
        u.executor_id = offer_data["executor_id"]


        db.session.add(u)
        db.session.commit()

        return "Order updated", 204
    if request.method == "DELETE":
        u = Order.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Order Deleted", 204



# база данных
def init_database(self):
    db.drop_all()
    db.create_all()

    for user_data in raw_data.users:
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )

        db.session.add(new_user)
        db.session.commit()

    for order_data in raw_data.orders:
        new_order = User(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"],
        )

        db.session.add(new_order)
        db.session.commit()

    for offer_data in raw_data.offers:
        new_offer = User(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"],
        )

        db.session.add(new_offer)
        db.session.commit()


if __name__ == '__main__':
    init_database()
    app.run(debug=True)

