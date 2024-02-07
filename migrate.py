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

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


if __name__ == "__main__":
    main()
    # Define column names and types
	table = {'customer':{'name':['','','',''],
			     'types':['','','',''],
			     'rows':10
			    },
		 'branch':{'name':['','','',''],
			     'types':['','','',''],
			   'rows':5
			    }
		
		}
	for i in table:
		data = {}
		num_rows = table[i]['rows']
		for name, dtype in zip( table[i]['name'],  table[i]['types']):
		

	
	df.to_sql(name=i, con=engine)
	
	column_names = ['ID', 'Name', 'Salary', 'Join_Date']
	column_types = [int, str, float, 'datetime64[ns]']
	num_rows = 10  # Number of rows for mock data
	
	# Generate mock data
	data = {}
	for name, dtype in zip(column_names, column_types):
	    if dtype == int:
	        data[name] = np.random.randint(1, 100, size=num_rows)
	    elif dtype == float:
	        data[name] = np.random.uniform(20000, 100000, size=num_rows)
	    elif dtype == str:
	        data[name] = ['Name_' + str(i) for i in range(1, num_rows+1)]
	    elif dtype == 'datetime64[ns]':
	        start_date = datetime(2020, 1, 1)
	        end_date = datetime(2022, 12, 31)
	        delta = end_date - start_date
	        random_dates = [start_date + timedelta(days=np.random.randint(delta.days)) for _ in range(num_rows)]
	        data[name] = random_dates
	
	# Create pandas DataFrame
	df = pd.DataFrame(data)
	
	# Display DataFrame
	# print(df)
	df.to_sql(name='customer', con=engine)
