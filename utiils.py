import json
from main import db
from main import User, Order, Offer
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
                            name=order['first_name'],
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


def all_guides(smt):
    return {
        'id' : smt.id,
        'surname' : smt.surname,
        'full_name' : smt.full_name,
        'tours_count' : smt.tours_count,
        'bio' : smt.bio,
        'is_pro' : smt.is_pro,
        'company' : smt.company
    }