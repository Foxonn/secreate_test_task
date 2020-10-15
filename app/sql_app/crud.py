import sqlalchemy
from sqlalchemy.orm import Session

from typing import List
from . import models, schemas


def _prepare_sku(value: str):
    return value.strip().replace(" ", "")


def _prepare_title(value: str):
    return value.strip()


def create_product(db: Session, group_id: int, product: schemas.ProductCreate):
    title = _prepare_title(product.dict().get("title"))
    sku = _prepare_sku(product.dict().get("sku"))

    if group_id:
        get_group(db, group_id)

    params = product.dict()

    params.update({"title": title, "sku": sku})

    db_product = models.Product(**params)
    db.add(db_product)
    db.commit()

    return db_product


def get_product(db: Session, sku: str = None, id: int = None):
    db_product = None

    if sku:
        sku = _prepare_sku(sku)
        db_product = db.query(models.Product).filter(models.Product.sku == sku).first()
    elif id and id >= 0:
        db_product = db.query(models.Product).filter(models.Product.id == id).first()

    if not db_product:
        raise sqlalchemy.orm.exc.NoResultFound(
            f'page {f"id: {id}" or f"sku: {sku}"} not found'
        )

    return db_product


def get_products(db: Session, group_id: int):
    db_products = db.query(models.Product)

    if group_id and get_group(db, group_id):
        db_products = db_products.filter(models.Product.group_id == group_id)

    return db_products.all()


def update_products(db: Session, products: list):
    db_products = db.query(models.Product)

    ids = [product.dict().get('id') for product in products
           if product.dict().get('id', None)]

    db_products = db_products.filter(models.Product.id.in_(ids))

    for product in products:
        id = product.dict().get('id')

        get_product(db, id=id)

        db_product = db_products.filter(models.Product.id == id).first()

        for field, value in product.dict().items():

            if field == 'id' or value is None:
                continue

            if field == 'group_id':
                get_group(db, group_id=value)

            if hasattr(db_product, field):
                setattr(db_product, field, value)

    db.commit()

    return db.query(models.Product).filter(models.Product.id.in_(ids)).all()


def update_product(db: Session, id: int, product: schemas.ProductUpdate):
    params = product.dict()

    if title := product.dict().get("title"):
        title = _prepare_title(title)
        params.update({"title": title})

    if sku := product.dict().get("sku"):
        sku = _prepare_sku(sku)
        params.update({"sku": sku})

    db_product = db.query(models.Product).filter(
        models.Product.id == id).first()

    for field, value in params.items():
        if value and hasattr(db_product, field):
            setattr(db_product, field, value)

    if db_product.reserved > db_product.remain:
        raise ValueError("invalid value `reserved` or `remain`")

    db.commit()

    return db_product


def delete_product(db: Session, id: int):
    db_product = db.query(models.Product).filter(
        models.Product.id == id).first()
    db.delete(db_product)
    db.commit()

    return db_product


def create_group(db: Session, group: schemas.GroupCreate):
    params = group.dict()

    params.update({'title': _prepare_title(group.dict().get("title"))})

    db_group = models.Group(**params)
    db.add(db_group)
    db.commit()

    return db_group


def get_group(db: Session, group_id: int):
    db_group = db.query(models.Group).filter(
        models.Group.id == group_id).first()

    if not db_group:
        raise sqlalchemy.orm.exc.NoResultFound(f'group_id: {group_id}')

    return db_group
