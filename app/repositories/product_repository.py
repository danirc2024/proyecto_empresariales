from sqlalchemy.orm import Session
from ..models.product import Product
from ..schemas.product import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_product(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_products(self, skip: int = 0, limit: int = 100):
        return self.db.query(Product).offset(skip).limit(limit).all()

    def create_product(self, product: ProductCreate):
        db_product = Product(**product.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update_product(self, product_id: int, product: ProductUpdate):
        db_product = self.get_product(product_id)
        if db_product:
            # Obtener solo los campos que fueron realmente proporcionados (no None)
            update_data = product.dict(exclude_unset=True, exclude_none=True)
            for key, value in update_data.items():
                setattr(db_product, key, value)
            self.db.commit()
            self.db.refresh(db_product)
        return db_product

    def delete_product(self, product_id: int):
        db_product = self.get_product(product_id)
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
        return db_product

