from sqlalchemy import Column, Integer, String, Float
from ..db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    customer_name = Column(String, index=True, default="Sin nombre")
    region = Column(String, default="Sin región")
    comuna = Column(String, default="Sin comuna")
    delivery_address = Column(String, default="Sin dirección")
    status = Column(String, default="pendiente") # pendiente, en proceso, entregado
