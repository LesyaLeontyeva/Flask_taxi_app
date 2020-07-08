"""ORM модель."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, \
    DateTime, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from typing import Any
from sqlalchemy.orm import sessionmaker

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
