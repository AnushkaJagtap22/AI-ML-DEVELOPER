from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas

from database import engine, SessionLocal

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency Injection
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Home Route
@app.get("/")
def home():
    return {"message": "FastAPI CRUD with SQLAlchemy"}


# CREATE PRODUCT
@app.post("/products")
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):

    new_product = models.Product(
        name=product.name,
        price=product.price,
        description=product.description,
        quantity=product.quantity
    )

    db.add(new_product)

    db.commit()

    db.refresh(new_product)

    return new_product


# FETCH ALL PRODUCTS
@app.get("/products")
def get_products(db: Session = Depends(get_db)):

    products = db.query(models.Product).all()

    return products


# FETCH SINGLE PRODUCT
@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return {"error": "Product not found"}

    return product


# UPDATE PRODUCT
@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    updated_product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return {"error": "Product not found"}

    product.name = updated_product.name
    product.price = updated_product.price
    product.description = updated_product.description
    product.quantity = updated_product.quantity

    db.commit()

    db.refresh(product)

    return product


# DELETE PRODUCT
@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        return {"error": "Product not found"}

    db.delete(product)

    db.commit()

    return {"message": "Product deleted successfully"}