from sqlalchemy import create_engine
from sqlalchemy import engine
from sqlalchemy.orm import declarative_base, Mapped, relationship
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
import pandas as pd

connection_url = engine.URL.create(
    drivername='mysql+pymysql',
    username='root',
    password='',
    host='localhost',
    database='gsmarena_data',
)

engine = create_engine(connection_url)

Base = declarative_base()


class Phone(Base):
    __tablename__ = 'phone'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    model = Column(String(128))
    year = Column(Integer)
    price = Column(Integer)
    Battery = Column(Integer)
    os_id = Column(Integer, ForeignKey('os.id'))
    weight = Column(Integer)
    sim = Column(String(16))
    size = Column(Integer)
    length_resolution = Column(Integer)
    width_resolution = Column(Integer)
    ppi = Column(Integer)
    ratio = Column(DECIMAL)
    length = Column(DECIMAL)
    width = Column(DECIMAL)
    thickness = Column(DECIMAL)


class Brand(Base):
    __tablename__ = 'brand'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))


class OS(Base):
    __tablename__ = 'os'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(16))
    version = Column(String(16))


class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))


class Phone_Sensor(Base):
    __tablename__ = 'phone_sensor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_id = Column(Integer, ForeignKey('phone.id'))
    sensor_id = Column(Integer, ForeignKey('sensor.id'))


class Memory(Base):
    __tablename__ = 'memory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    Ram = Column(Integer)
    main_memory = Column(Integer)


class Phone_Memory(Base):
    __tablename__ = 'phone_memory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_id = Column(Integer, ForeignKey('phone.id'))
    memory_id = Column(Integer, ForeignKey('memory.id'))

class Network(Base):
    __tablename__ = 'network'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))

class Phone_Network(Base):
    __tablename__ = 'phone_network'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_id = Column(Integer, ForeignKey('phone.id'))
    network_id = Column(Integer, ForeignKey('network.id'))


Base.metadata.create_all(engine)

phone = pd.read_csv('db_datas/phone.csv')
os = pd.read_csv('db_datas/os.csv')
brand = pd.read_csv('db_datas/brand.csv')
sensor = pd.read_csv('db_datas/sensor.csv')
phone_sensor = pd.read_csv('db_datas/phone-sensor.csv')
memory = pd.read_csv('db_datas/memory.csv')
phone_memory = pd.read_csv('db_datas/phone-memory.csv')
network = pd.read_csv('db_datas/network.csv')
phone_network = pd.read_csv('db_datas/phone_network.csv')

network.to_sql('network', con=engine, if_exists='append', index=False)
brand.to_sql('brand', con=engine, if_exists='append', index=False)
sensor.to_sql('sensor', con=engine, if_exists='append', index=False)
os.to_sql('os', con=engine, if_exists='append', index=False)
memory.to_sql('memory', con=engine, if_exists='append', index=False)
phone.to_sql('phone', con=engine, if_exists='append', index=False)
phone_sensor.to_sql('phone_sensor', con=engine, if_exists='append', index=False)
phone_memory.to_sql('phone_memory', con=engine, if_exists='append', index=False)
phone_network.to_sql('phone_network', con=engine, if_exists='append', index=False)
