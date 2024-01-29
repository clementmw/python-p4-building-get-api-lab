#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    get_bakeries  = Bakery.query.all()
    dict_bakery  = [n.to_dict() for n in get_bakeries]
    response   = make_response(jsonify(dict_bakery), 200)
    # response.headers["Content-Type"] = "application/json"
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    by_id = Bakery.query.filter_by(id = id).first()

    if not by_id:
        response = make_response(jsonify({'error': 'Bakery not found'}), 404)
        return response
    else:
        by_dict = by_id.to_dict()
        response = make_response(jsonify(by_dict), 200)
        return response
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    get_goods = BakedGood.query.order_by(desc(BakedGood.price)).all()

    goods_dict = [n.to_dict() for n in get_goods]
    response = make_response(jsonify(goods_dict), 200)
    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive = BakedGood.query.order_by(desc(BakedGood.price)).first()
    
    sort = expensive.to_dict()
    response = make_response(jsonify(sort), 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
