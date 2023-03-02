from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    costumers = relationship('User', foreign_keys=[customer_id])
    executors = relationship('User', foreign_keys=[executor_id])


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    orders = relationship('Order', foreign_keys=[order_id])
    executors = relationship('User', foreign_keys=[executor_id])


def open_users():
    sm = []
    with open('data/users.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for user in data:
            sm.append(User(id=user['id'],
                           first_name=user['first_name'],
                           last_name=user['last_name'],
                           age=user['age'],
                           email=user['email'],
                           role=user['role'],
                           phone=user['phone']))
    db.session.add_all(sm)
    db.session.commit()


def open_orders():
    sm = []
    with open('data/orders.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for order in data:
            sm.append(Order(id=order['id'],
                            name=order['name'],
                            description=order['description'],
                            start_date=order['start_date'],
                            end_date=order['end_date'],
                            address=order['address'],
                            price=order['price'],
                            customer_id=order['customer_id'],
                            executor_id=order['executor_id']))
    db.session.add_all(sm)
    db.session.commit()


def open_offers():
    sm = []
    with open('data/offers.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for offer in data:
            sm.append(Offer(id=offer['id'], order_id=offer['order_id'], executor_id=offer['executor_id']))
    db.session.add_all(sm)
    db.session.commit()


def all_users(smt):
    return {
        'id': smt.id,
        'first_name': smt.first_name,
        'last_name': smt.last_name,
        'age': smt.age,
        'email': smt.email,
        'role': smt.role,
        'phone': smt.phone
    }


db.drop_all()
db.create_all()
open_users()
open_offers()
open_orders()


@app.route('/users')
def get_all_users():
    a = []
    users = User.query.all()
    for user in users:
        a.append(all_users(user))
    return jsonify(a)


@app.route('/users/<int:id>')
def user_by_id(id):
    us = all_users(User.query.filter(User.id == id).one())
    return jsonify(us)


def all_offers(smt):
    return {
        'id': smt.id,
        'order_id': smt.order_id,
        'executor_id': smt.executor_id,
    }


@app.route('/offers')
def get_all_offers():
    a = []
    offers = Offer.query.all()
    for offer in offers:
        a.append(all_offers(offer))
    return jsonify(a)


@app.route('/offers/<int:id>')
def offer_by_id(id):
    of = all_offers(Offer.query.filter(Offer.id == id).one())
    return jsonify(of)


def all_orders(smt):
    return {
        'id': smt.id,
        'name': smt.name,
        'description': smt.description,
        'end_date': smt.end_date,
        'address': smt.address,
        'price': smt.price,
        'customer_id': smt.customer_id,
        'executor_id': smt.executor_id
    }


@app.route('/orders')
def get_all_orders():
    a = []
    orders = Order.query.all()
    for order in orders:
        a.append(all_orders(order))
    return jsonify(a)


@app.route('/orders/<int:idd>')
def order_by_id(idd):
    orr = all_orders(Order.query.filter(Order.id == idd).one())
    return jsonify(orr)


# @app.route("/guides/<int:gid>/delete")
# def delete_guide(gid):
#     guide = Guide.query.get(gid)
#     db.session.delete(guide)
#     db.session.commit()
#     return jsonify("")


@app.route('/users', methods=['POST'])
def add_user():
    use = request.json
    us = User(
        id=use.get('id'),
        first_name=use.get('first_name'),
        last_name=use.get('last_name'),
        age=use.get('age'),
        email=use.get('email'),
        role=use.get('role'),
        phone=use.get('phone')
    )
    db.session.add(us)
    db.session.commit()
    return jsonify(all_users(us))


@app.route('/users/<int:id>', methods=['PUT'])
def renew_user(id):
    use = request.json
    user = User.query.get(id)
    user.first_name = use.get('first_name')
    user.last_name = use.get('last_name')
    user.age = use.get('age')
    user.email = use.get('email')
    user.role = use.get('role')
    user.phone = use.get('phone')
    db.session.add(user)
    db.session.commit()
    return jsonify(all_users(user))



@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify("")

# ruuuu

@app.route('/offers', methods=['POST'])
def add_offer():
    off = request.json
    of = Offer(
        id=off.get('id'),
        order_id=off.get('order_id'),
        executor_id=off.get('executor_id'),
    )
    db.session.add(of)
    db.session.commit()
    return jsonify(all_offers(of))

@app.route('/offers/<int:id>', methods=['PUT'])
def renew_offers(id):
    off = request.json
    offer = Offer.query.get(id)
    offer.order_id = off.get('order_id')
    offer.executor_id = off.get('executor_id')

    db.session.add(offer)
    db.session.commit()
    return jsonify(all_offers(offer))


@app.route('/offers/<int:id>', methods=['DELETE'])
def delete_offer(id):
    offer = Offer.query.get(id)
    db.session.delete(offer)
    db.session.commit()
    return jsonify("")


# ruurururur


@app.route('/orders', methods=['POST'])
def add_orders():
    ordd = request.json
    oor = Order(
        id=ordd.get('id'),
        name=ordd.get('name'),
        description=ordd.get('description'),
        start_date=ordd.get('start_date'),
        end_date=ordd.get('end_date'),
        address=ordd.get('address'),
        price=ordd.get('price'),
        customer_id=ordd.get('customer_id'),
        executor_id=ordd.get('executor_id'),
    )
    db.session.add(oor)
    db.session.commit()
    return jsonify(all_orders(oor))


@app.route('/orders/<int:id>', methods=['PUT'])
def renew_order(id):
    urde = request.json
    order = Order.query.get(id)
    print(order)
    print(urde.get('name'))
    order.name = urde.get('name')
    order.description = urde.get('description')
    order.start_date = urde.get('start_date')
    order.end_date = urde.get('end_date')
    order.address = urde.get('address')
    order.price = urde.get('price')
    order.customer_id = urde.get('customer_id')
    order.executor_id = urde.get('executor_id')
    db.session.add(order)
    db.session.commit()
    return jsonify(all_orders(order))

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify("")


if __name__ == '__main__':
    app.run()
