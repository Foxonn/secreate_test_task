from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True, unique=True, nullable=False)

    products = relationship("Product", back_populates="group")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(75), index=True, nullable=False)
    sku = Column(String(16), index=True, unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"))
    remain = Column(Integer, nullable=False, default=0)
    reserved = Column(Integer, nullable=False, default=0)

    group = relationship("Group", back_populates="products")

