from fastapi import Query
from typing import List
from pydantic import BaseModel


class BaseProduct(BaseModel):
    title: str = Query(..., min_length=3, max_length=75)
    sku: str = Query(..., min_length=3, max_length=16)
    remain: int = Query(..., gt=0, le=999999)


class ProductUpdate(BaseModel):
    title: str = Query(None, min_length=3, max_length=75)
    sku: str = Query(None, min_length=3, max_length=16)
    remain: int = Query(None, gt=0, le=999999)
    reserved: int = Query(None, gt=0, le=999999)
    group_id: int = Query(None, gt=0, le=999999)

    class Config:
        schema_extra = {
            "example": [
                {
                    "sku": "465KL55",
                    "title": "item 1"
                },
                {
                    "sku": "465KL55",
                }
            ]
        }


class ProductsUpdate(ProductUpdate):
    id: int

    class Config:
        schema_extra = {
            "example": [
                {
                    "id": 1,
                    "sku": "465KL55",
                    "title": "item 1"
                },
                {
                    "id": 2,
                    "sku": "465KL55",
                }
            ]
        }


class ProductCreate(BaseProduct):
    group_id: int = Query(..., gt=0, le=999999)


class Product(BaseProduct):
    id: int
    reserved: int
    group_id: int

    class Config:
        orm_mode = True


class Group(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class GroupCreate(BaseModel):
    title: str = Query(..., min_length=3, max_length=75)


class GroupGet(BaseModel):
    id: int
    title: str
    products: List[Product]

    class Config:
        orm_mode = True
