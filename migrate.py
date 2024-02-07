
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine
import os
import datetime
import names
import pandas as pd
import numpy as np
from datetime import timedelta

class Customer(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	sex: str
	address_province: str
	register_date: datetime.datetime = Field(default=datetime.datetime.now(), nullable=True)

class Branch(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	address_province: str 

class Employee(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	sex:str
	address_province: str 
	register_date:  datetime.datetime = Field(default=datetime.datetime.now(), nullable=True)
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

# password must not contain @
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DBconnection") 
engine = create_engine(DATABASE_URL
					,pool_size=10,
									max_overflow=2,
									pool_recycle=300,
									pool_pre_ping=True,
									pool_use_lifo=True
									, isolation_level="AUTOCOMMIT")
def create_table():
	SQLModel.metadata.drop_all(engine)
	SQLModel.metadata.create_all(engine)

def create_record():
	table = {
		'branch':{'name':['id','name','address_province'],
			     'types':[int,str,str],
			     'rows':10
			    },
		'categories':{'name':['id','name'],
			     'types':[int,str],
			   'rows':5
			    }
		}
	for i in table:
		data={}
		num_rows = table[i]['rows']
		for name,dtype in zip(table[i]['name'],table[i]['types']):
			if name == 'id':
				data[name] = range(0, num_rows, 1)
			elif dtype == int:
				data[name] = np.random.randint(1, 100, size=num_rows)
			elif dtype == float:
				data[name] = np.random.uniform(20000, 100000, size=num_rows)
			elif dtype == str:
				if name == 'name':
					data[name] = [ names.get_full_name()  for i in range(1, num_rows+1)] 
				else:
					data[name] = ['Name_' + str(i) for i in range(1, num_rows+1)]
			elif dtype == 'datetime64[ns]':
				start_date = datetime(2020, 1, 1)
				end_date = datetime(2022, 12, 31)
				delta = end_date - start_date
				random_dates = [start_date + timedelta(days=np.random.randint(delta.days)) for _ in range(num_rows)]
				data[name] = random_dates
		df = pd.DataFrame(data)
		df.to_sql(i, con=engine, if_exists='append',index=False)





if __name__ == "__main__":
	create_table()
	create_record()