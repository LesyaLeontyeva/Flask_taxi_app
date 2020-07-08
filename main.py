"""
Домашняя работа по flask.

Веб-приложение по заказу такси.
"""
import json
from datetime import datetime
from ORM_model import Session, Drivers, Orders, Client
from flask import Flask, request, make_response, abort, Response

app = Flask(__name__)


@app.route('/drivers', methods=['POST'])
def post_driver() -> Response:
    """Метод по созданию водителя."""
    request_body = json.loads(request.data)
    name = request_body['name']
    car = request_body['car']
    posted_driver = Drivers(None, name, car)
    session = Session()
    session.add(posted_driver)
    session.commit()
    return make_response('added')


@app.route('/drivers', methods=['GET'])
def get_drivers() -> Response:
    """Метод по получению списка водителей."""
    driverId = request.args.get('driverId')
    session = Session()
    got_driver = session.query(Drivers). \
        filter_by(id=driverId).first()
    json_from_db = {'id': got_driver.id, 'name': got_driver.name,
                    'car': got_driver.car}
    return make_response(json_from_db)


@app.route('/drivers/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id: int) -> Response:
    """Метод по удалению водителя."""
    session = Session()
    deleted_driver = session.query(Drivers).filter_by(id=driver_id).first()
    session.delete(deleted_driver)
    session.commit()
    return make_response('deleted')


@app.route('/clients', methods=['POST'])
def post_client() -> Response:
    """Метод по созданию клиента."""
    request_body = json.loads(request.data)
    name = request_body['name']
    is_vip = request_body['is_vip']
    posted_client = Client(None, name, is_vip)
    session = Session()
    session.add(posted_client)
    session.commit()
    return make_response('added')


@app.route('/clients', methods=['GET'])
def get_client() -> Response:
    """Метод по получению клиентов по id."""
    clientId = request.args.get('clientId')
    session = Session()
    got_client = session.query(Client).filter_by(id=clientId).first()
    json_from_db = {'id': got_client.id, 'name': got_client.name,
                    'is_vip': got_client.is_vip}
    return make_response(json_from_db)


@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id: int) -> Response:
    """Метод по удалению клиента."""
    session = Session()
    deleted_client = session.query(Client).filter_by(id=client_id).first()
    session.delete(deleted_client)
    session.commit()
    return make_response('deleted')


@app.route('/orders', methods=['POST'])
def post_order() -> Response:
    """Метод по созданию заказа."""
    request_body = json.loads(request.data)
    address_from = request_body['address_from']
    address_to = request_body['address_to']
    client_id = request_body['client_id']
    driver_id = request_body['driver_id']
    date_created = datetime.strptime(request_body['date_created'],
                                     '%Y-%m-%dT%H:%M:%S.%fZ')
    status = request_body['status']
    posted_order = Orders(None, address_from, address_to,
                          client_id, driver_id, date_created, status)
    session = Session()
    session.add(posted_order)
    session.commit()
    return make_response('added')


@app.route('/orders', methods=['GET'])
def get_order() -> Response:
    """Метод по получению заказов."""
    orderId = request.args.get('orderId')
    session = Session()
    got_order = session.query(Orders).filter_by(id=orderId).first()
    json_from_db = {'id': got_order.id, 'address_from': got_order.address_from,
                    'address_to': got_order.address_to,
                    'client_id': got_order.client_id,
                    'driver_id': got_order.driver_id,
                    'date_created': got_order.date_created,
                    'status': got_order.status}
    return make_response(json_from_db)


@app.route('/orders/<int:order_id>', methods=['PUT'])
def put_order(order_id: int) -> Response:
    """Метод по апдейту заказа."""
    session = Session()
    got_order = session.query(Orders). \
        filter_by(id=order_id).first()
    request_body = json.loads(request.data)
    flag = True
    update_dict = {}

    if request_body['status'] != got_order.status:
        if got_order.status == 'not_accepted' \
                and request_body['status'] == 'done':
            flag = False
        elif got_order.status == 'in_progress' and \
                request_body['status'] == 'not_accepted':
            flag = False
        elif got_order.status in ('done', 'cancelled'):
            flag = False
        else:
            status = request_body['status']
            update_dict['status'] = status

    if request_body['date_created'] != got_order.date_created:
        if got_order.status == 'not_accepted':
            date_created = datetime.strptime(request_body['date_created'],
                                             '%Y-%m-%dT%H:%M:%S.%fZ')
            update_dict['date_created'] = date_created
        else:
            flag = False

    if request_body['client_id'] != got_order.client_id:
        if got_order.status == 'not_accepted':
            client_id = request_body['client_id']
            update_dict['client_id'] = client_id
        else:
            flag = False

    if request_body['driver_id'] != got_order.driver_id:
        if got_order.status == 'not_accepted':
            driver_id = request_body['driver_id']
            update_dict['driver_id'] = driver_id
        else:
            flag = False

    if flag:
        session = Session()
        session.query(Orders).filter_by(id=order_id). \
            update(update_dict)
        session.commit()
        return make_response('changed')
    else:
        abort(403, 'not allowed')


app.run()
