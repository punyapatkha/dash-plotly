
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine
import os
import datetime
import names
import pandas as pd
import numpy as np
from datetime import timedelta
import random

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
	# branch_id: Optional[int] = Field(default=None, foreign_key="branch.id")

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
	total_price: int
	employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")
	branch_id: Optional[int] = Field(default=None, foreign_key="branch.id")
	cust_id: Optional[int] = Field(default=None, foreign_key="customer.id")
	tran_date: datetime.datetime = Field(default=datetime.datetime.now(), nullable=True)

class Order(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	price: int
	amount: int
	amount_price: int	
	product_id: Optional[int] = Field(default=None, foreign_key="product.id")
	tran_id: Optional[int] = Field(default=None, foreign_key="transaction.id")


from utils.db import DBengine

engine = DBengine

def create_table():
	SQLModel.metadata.drop_all(engine)
	SQLModel.metadata.create_all(engine)

def create_fixed_record():
	data = {
	"categories":{
	# "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	# "name": ["Apparel and Accessories",
	# 	"Electronics and Appliances",
	# 	"Home and Furniture",
	# 	"Health and Beauty",
	# 	"Grocery and Food Items",
	# 	"Toys and Games",
	# 	"Sports and Fitness Equipment",
	# 	"Automotive and Tools",1600 24 4m 800k
	# 	"Books and Stationery",
	# 	"Home Improvement and Gardening"10% contract break contact blacklist
	# 	   ],
	"id": [1, 2, 3, 4],
	"name": ["Apparel and Accessories",
		"Home and Furniture",
		"Grocery and Food Items",
		"Sports and Fitness Equipment"
		   ]
	},
	"branch":{	
	"id": [1, 2, 3],
	"name": ["Central_Branch", "Nowhere_Branch", "South_Branch"],
	"address_province": ["A_province", "B_province", "C_province"]
	},
	"product":{
	"id": [1, 2, 3, 4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12],
	"name": ["Shirt", "Hat", "Trousers","Stool" ,"Hammer" ,"Egg" ,"Apple" ,"Meat" ,"Milk" ,"Rice" ,"Soda" ,"Running Shoes"],
	"unit_price": [150, 100, 300, 500 ,200 ,20 ,13 ,30 ,30 ,14 ,15 ,400],
	"cat_id": [1, 1, 1, 2 ,2 ,3 ,3 ,3 ,3 ,3 ,3 ,4]
	}

	
	}
	for i in data:
		df = pd.DataFrame(data[i])
		df.to_sql(i, con=engine, if_exists='append',index=False)

def create_random_record():
	address_province = ["A_province", "B_province", "C_province"]
	sex = ["male", "female", "undefined"]
	
	table = {
		'customer':{'name':['id','name','sex','address_province','register_date'],
			     'types':[int,str,str,str,'datetime64[ns]'],
			     'rows':300
			    },
		'employee':{'name':['id','name','sex','address_province','register_date'],
			     'types':[int,str,str,str,'datetime64[ns]'],
			     'rows':30
			    },
		'transaction':{'name':['id','total_price','employee_id','branch_id','cust_id','tran_date'],
			     'types':[int,int,int,int,int,'datetime64[ns]'],
			     'rows':1000
			    },
		'order':{'name':['id','price','amount','amount_price','product_id','tran_id'],
			     'types':[int,int,int,int,int,int],
			     'rows':5000
			    },


		}
	for i in table:
		data={}
		num_rows = table[i]['rows']
		for name,dtype in zip(table[i]['name'],table[i]['types']):
			if name == 'id':
				data[name] = range(1, num_rows+1, 1)
			elif dtype == int:
				if name == 'employee_id':
					data[name] = np.random.randint(1, table['employee']['rows']+1, size=num_rows)
				elif name == 'cust_id':
					data[name] = np.random.randint(1, table['customer']['rows']+1, size=num_rows)
				elif name == 'product_id':
					# fixed 12 product
					data[name] = np.random.randint(1, 12+1, size=num_rows)
				elif name == 'tran_id':
					data[name] = np.random.randint(1, table['transaction']['rows']+1, size=num_rows)
				elif name == 'branch_id':
					# fixed 3 branch
					data[name] = np.random.randint(1, 3+1, size=num_rows)
				elif name == 'total_price':
					data[name] = np.random.randint(500,5000, size=num_rows)
				elif name == 'amount':
					data[name] = np.random.randint(1,5, size=num_rows)
				else:
					data[name] = np.random.randint(1, 100, size=num_rows)
			elif dtype == float:
				data[name] = np.random.uniform(20000, 100000, size=num_rows)
			elif dtype == str:
				if name == 'name':
					# https://stackoverflow.com/questions/5893163/what-is-the-purpose-of-the-single-underscore-variable-in-python
					# _ for throwaway variables.
					data[name] = [ names.get_full_name()  for _ in range(1, num_rows+1)] 
				elif name == 'address_province':
					data[name] = [ random.choice(address_province)  for _ in range(1, num_rows+1)] 
				elif name == 'sex':
					data[name] = [ random.choice(sex)  for _ in range(1, num_rows+1)] 
				else:
					data[name] = ['Name_' + str(i) for i in range(1, num_rows+1)]
			elif dtype == 'datetime64[ns]':
				start_date = datetime.datetime(2023, 1, 1)
				end_date = datetime.datetime(2024, 2, 20)
				delta = end_date - start_date
				random_dates = [start_date + timedelta(days=np.random.randint(delta.days)) for _ in range(num_rows)]
				data[name] = random_dates
		df = pd.DataFrame(data)
		df.to_sql(i, con=engine, if_exists='append',index=False)


def update_record():
	from sqlalchemy.sql import text
	with engine.connect() as con:
		statement1 = text("""
					UPDATE "order"
					SET price=subquery.unit_price
					FROM (SELECT b.unit_price ,b.id
					FROM  product b ) AS subquery
					WHERE "order".product_id=subquery.id;
					""")
		con.execute(statement1)
		con.commit()
		
		statement1 = text("""
					UPDATE "order"		
					SET amount = 	case when "order".price > 100 then floor(random()* (3-1 + 1) + 1)
					else floor(random()* (10-1 + 1) + 1) END
					-- floor(random()* (high-low + 1) + low)
					
					""")
		con.execute(statement1)
		con.commit()

		statement2 = text("""
					UPDATE "order"
					SET amount_price = amount*price
					""")
		con.execute(statement2)
		con.commit()
		
		statement3 = text("""
					UPDATE "transaction"
					SET total_price=subquery.sum_order
					FROM (SELECT sum(b.amount_price) as sum_order ,b.tran_id
					FROM  "order" b 
					group by b.tran_id
					) AS subquery
					WHERE subquery.tran_id=transaction.id;
					""")
		con.execute(statement3)
		con.commit()

		statement4 = text("""
					Delete from "transaction" 
					WHERE "transaction".id not in (select b.tran_id from "order" b);
					""")
		con.execute(statement4)
		con.commit()

# with engine.connect() as con:

#     data = ( { "id": 1, "title": "The Hobbit", "primary_author": "Tolkien" },
#              { "id": 2, "title": "The Silmarillion", "primary_author": "Tolkien" },
#     )

#     statement = text("""INSERT INTO book(id, title, primary_author) VALUES(:id, :title, :primary_author)""")

#     for line in data:
#         con.execute(statement, **line)



if __name__ == "__main__":
	create_table()
	create_fixed_record()
	create_random_record()
	update_record()