from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    customer_name: Optional[str] = "Sin nombre"
    region: Optional[str] = "Sin región"
    comuna: Optional[str] = "Sin comuna"
    delivery_address: Optional[str] = "Sin dirección"
    status: Optional[str] = "pendiente"

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
