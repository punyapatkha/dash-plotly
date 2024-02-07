from typing import Optional

from typing import List, Optional
from sqlalchemy import Column,Integer,String
from config import Base,engine
from sqlmodel import Field, Session, SQLModel, create_engine, select

import datetime
import random
from random import randrange
from datetime import timedelta

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
  	sex: str
	  address_province: str 
    register_date: datetime

class Branch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
	  address_province: str 

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
	  sex: str
	  address_province: str 
    register_date: datetime
	  branch_id: Optional[int] = Field(default=None, foreign_key="branch.id")

class Categories(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
	
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    unit_price: int
    cat_id: Optional[int] = Field(default=None, foreign_key="categories.id")
	
class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    unit_price: int
	
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")
	  branch_id: Optional[int] = Field(default=None, foreign_key="branch.id")
	  cust_id: Optional[int] = Field(default=None, foreign_key="customer.id")
	
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    price: int
    amount: int
    amount_price: int	
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
	  tran_id: Optional[int] = Field(default=None, foreign_key="transaction.id")

def main():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    main()
