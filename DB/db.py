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
    database='',
)

engine = create_engine(connection_url)

Base = declarative_base()


class Phone(Base):
    __tablename__ = 'phone'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    name = Column(String(128))
    year = Column(Integer)
    price = Column(Integer)
    Battery = Column(Integer)
    network = Column(String(3))
    os_id = Column(Integer, ForeignKey('os.id'))
    weight = Column(Integer)
    sim = Column(String(16))
    size = Column(Integer)
    resolution = Column(String(16))
    ppi = Column(Integer)
    ratio = Column(DECIMAL)
    dimension = Column(String(16))


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


Base.metadata.create_all(engine)


phone = pd.read_csv('phone_data.csv')
os = pd.read_csv('os_data.csv')
brand = pd.read_csv('brand_data.csv')
sensor = pd.read_csv('sensor_data.csv')
phone_sensor = pd.read_csv('phone_sensor_data.csv')
memory = pd.read_csv('memory.csv')
phone_memory = pd.read_csv('phone_memory_data.csv')


phone.to_sql('phone', con=engine, if_exists='append', index=False)
os.to_sql('os', con=engine, if_exists='append', index=False)
brand.to_sql('brand', con=engine, if_exists='append', index=False)
sensor.to_sql('sensor', con=engine, if_exists='append', index=False)
phone_sensor.to_sql('phone_sensor', con=engine, if_exists='append', index=False)
memory.to_sql('memory', con=engine, if_exists='append', index=False)
phone_memory.to_sql('phone_memory', con=engine, if_exists='append', index=False)
