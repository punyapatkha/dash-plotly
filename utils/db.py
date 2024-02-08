import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def printa(text):
    return "abc"+str(text)+"abc"

load_dotenv()
DATABASE_URL=os.getenv("DBconnection") 
DBengine = create_engine(DATABASE_URL
					,pool_size=10,
									max_overflow=2,
									pool_recycle=300,
									pool_pre_ping=True,
									pool_use_lifo=True
									, isolation_level="AUTOCOMMIT")

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=DBengine)
Base = declarative_base()