from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse

import sqlalchemy
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine

from sql_app import schemas, crud, models
from typing import List
from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/product/", response_model=schemas.Product)
async def create_product(
        *,
        product: schemas.ProductCreate,
        db: Session = Depends(get_db)
):
    sku = product.dict().get('sku')
    group_id = product.dict().get('group_id')

    try:
        crud.get_product(db, sku=sku)
    except sqlalchemy.orm.exc.NoResultFound:
        pass
    else:
        raise HTTPException(
            status_code=400,
            detail=f"sku `{sku}` already exist"
        )

    try:
        return crud.create_product(db, group_id=group_id, product=product)
    except sqlalchemy.orm.exc.NoResultFound:
        raise HTTPException(
            status_code=400,
            detail=f"group_id `{group_id}` not found"
        )


@app.get("/product/", response_model=schemas.Product)
async def get_product(
        id: int,
        db: Session = Depends(get_db)
):
    try:
        db_product = crud.get_product(db, id=id)
    except sqlalchemy.orm.exc.NoResultFound as err:
        raise HTTPException(status_code=400, detail=ascii(err))

    return db_product


@app.delete("/product/")
async def delete_product(
        id: int,
        db: Session = Depends(get_db),
):
    db_product = crud.get_product(db, id=id)

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail=f"product not found"
        )

    db_product = crud.delete_product(db, id=id)

    if db_product:
        return JSONResponse(status_code=200, content="success")

    return JSONResponse(status_code=200, content="failure")


@app.put("/product/", response_model=schemas.Product)
async def update_product(
        id: int,
        product: schemas.ProductUpdate,
        db: Session = Depends(get_db),
):
    db_product = crud.get_product(db, id=id)

    if not db_product:
        raise HTTPException(status_code=404, detail=f"product not found")

    try:
        db_product = crud.update_product(db, id=id, product=product)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=ascii(err))

    return db_product


@app.get("/products/")
async def get_products(
        *,
        db: Session = Depends(get_db),
        group_id: Optional[int] = None,
):
    try:
        return crud.get_products(db, group_id=group_id)
    except sqlalchemy.orm.exc.NoResultFound as err:
        raise HTTPException(status_code=400, detail=err)


@app.put("/products/")
async def update_products(
        *,
        db: Session = Depends(get_db),
        products: List[schemas.ProductsUpdate],
):
    try:
        db_products = crud.update_products(db, products=products)
    except sqlalchemy.exc.IntegrityError as err:
        raise HTTPException(status_code=400, detail=ascii(err))

    except sqlalchemy.orm.exc.NoResultFound as err:
        raise HTTPException(status_code=400, detail=ascii(err))

    return db_products


@app.post("/group/", response_model=schemas.Group)
async def create_group(
        group: schemas.GroupCreate,
        db: Session = Depends(get_db)
):
    title = group.dict().get('title')

    try:
        db_group = crud.create_group(db, group=group)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"`title` '{title}' not unique"
        )

    return db_group


@app.get("/group/", response_model=schemas.GroupGet)
async def get_group(
        id: int,
        db: Session = Depends(get_db)
):
    db_group = crud.get_group(db, group_id=id)

    if not db_group:
        raise HTTPException(status_code=400, detail=f"group not found")

    return db_group
