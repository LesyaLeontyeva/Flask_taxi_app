"""Веб-приложение по заказу такси."""
import json
from datetime import datetime
from typing import Any

from flask import Flask, request, make_response, abort, Response
from sqlalchemy import Column, Integer, String, Boolean, \
    DateTime, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine("sqlite:///orchid_taxi.db", echo=True)
Base: Any = declarative_base()

Session = sessionmaker(bind=engine)


class Client(Base):
    """Модель под табличку с клиентами."""

    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, autoincrement=True,
                comment="Идентификатор заказа")
    name = Column(String, nullable=False, comment="Имя клиента")
    is_vip = Column(Boolean, nullable=False, comment="статус клиента")

    def __init__(self, id: Any, name: str, is_vip: bool) -> None:
        """__init__ метод."""
        self.id = id
        self.name = name
        self.is_vip = is_vip


class Drivers(Base):
    """Create model for table."""

    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    car = Column(String, nullable=False)

    def __init__(self, id: Any, name: str, car: str) -> None:
        """__init__ метод."""
        self.id = id
        self.name = name
        self.car = car


class Orders(Base):
    """Модель таблицы Orders."""

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_from = Column(String, nullable=False)
    address_to = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    date_created = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    def __init__(self, id: Any, address_from: str, address_to: str,
                 client_id: int, driver_id: int,
                 date_created: datetime, status: str) -> None:
        """__init__ метод."""
        self.id = id
        self.address_from = address_from
        self.address_to = address_to
        self.client_id = client_id
        self.driver_id = driver_id
        self.date_created = date_created
        self.status = status


Base.metadata.create_all(engine)


@app.route('/drivers', methods=['POST'])
def post_driver() -> Response:
    """Метод по созданию водителя."""
    dict1 = json.loads(request.data)
    name = dict1['name']
    car = dict1['car']
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
    dict1 = {'id': got_driver.id, 'name': got_driver.name,
             'car': got_driver.car}
    return make_response(dict1)


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
    dict1 = json.loads(request.data)
    name = dict1['name']
    is_vip = dict1['is_vip']
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
    dict1 = {'id': got_client.id, 'name': got_client.name,
             'is_vip': got_client.is_vip}
    return make_response(dict1)


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
    dict1 = json.loads(request.data)
    address_from = dict1['address_from']
    address_to = dict1['address_to']
    client_id = dict1['client_id']
    driver_id = dict1['driver_id']
    date_created = datetime.strptime(dict1['date_created'],
                                     '%Y-%m-%dT%H:%M:%S.%fZ')
    status = dict1['status']
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
    dict1 = {'id': got_order.id, 'address_from': got_order.address_from,
             'address_to': got_order.address_to,
             'client_id': got_order.client_id,
             'driver_id': got_order.driver_id,
             'date_created': got_order.date_created,
             'status': got_order.status}
    return make_response(dict1)


@app.route('/orders/<int:order_id>', methods=['PUT'])
def put_order(order_id: int) -> Response:
    """Метод по апдейту заказа."""
    session = Session()
    got_order = session.query(Orders). \
        filter_by(id=order_id).first()  # получили заказ из базы
    dict1 = json.loads(request.data)  # получили измененный заказ из запроса
    flag = True
    update_dict = {}

    if dict1['status'] != got_order.status:
        if got_order.status == 'not_accepted' and dict1['status'] == 'done':
            status = got_order.status
            flag = False
        elif got_order.status == 'in_progress' and \
                dict1['status'] == 'not_accepted':
            status = got_order.status
            flag = False
        elif got_order.status in ('done', 'cancelled'):
            status = got_order.status
            flag = False
        else:
            status = dict1['status']
            update_dict['status'] = status
    else:
        status = got_order.status

    if dict1['date_created'] != got_order.date_created:
        if got_order.status == 'not_accepted':
            date_created = datetime.strptime(dict1['date_created'],
                                             '%Y-%m-%dT%H:%M:%S.%fZ')
            update_dict['date_created'] = date_created
        else:
            date_created = got_order.date_created
            flag = False
    else:
        date_created = got_order.date_created

    if dict1['client_id'] != got_order.client_id:
        if got_order.status == 'not_accepted':
            client_id = dict1['client_id']
            update_dict['client_id'] = client_id
        else:
            client_id = got_order.client_id
            flag = False
    else:
        client_id = got_order.client_id

    if dict1['driver_id'] != got_order.driver_id:
        if got_order.status == 'not_accepted':
            driver_id = dict1['driver_id']
            update_dict['driver_id'] = driver_id
        else:
            driver_id = got_order.driver_id
            flag = False
    else:
        driver_id = dict1['driver_id']

    if flag:
        session = Session()
        session.query(Orders).filter_by(id=order_id). \
            update(update_dict)
        session.commit()
        return make_response('changed')
    else:
        abort(403, 'not allowed')


app.run()
