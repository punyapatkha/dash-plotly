import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
load_dotenv()



DATABASE_URL=os.getenv("DBconnection") 

db = SQLDatabase.from_uri(DATABASE_URL)

# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.run("SELECT * FROM branch LIMIT 10;"))

from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

# import getpass

# os.environ["OPENAI_API_KEY"] = getpass.getpass()

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "can you summarize each branch sales in each month with no limit"})
print(response)
print(db.run(response))