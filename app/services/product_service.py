from sqlalchemy.orm import Session
from ..repositories.product_repository import ProductRepository
from ..schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def get_product(self, product_id: int):
        return self.repository.get_product(product_id)

    def get_products(self, skip: int = 0, limit: int = 100):
        return self.repository.get_products(skip=skip, limit=limit)

    def create_product(self, product: ProductCreate):
        return self.repository.create_product(product)

    def update_product(self, product_id: int, product: ProductUpdate):
        return self.repository.update_product(product_id, product)

    def delete_product(self, product_id: int):
        return self.repository.delete_product(product_id)
