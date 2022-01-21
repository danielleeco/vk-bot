from sqlalchemy import Column, Integer, Float, String
from .database import Base


class Sections(Base):
    __tablename__ = 'sections'

    section = Column(String, primary_key=True, index=True)


class Products(Base):
    __tablename__ = 'products'
    id_prod = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    section = Column(String)
    product_name = Column(String)
    price = Column(Float)
    weight = Column(Float)
    picture = Column(String)
