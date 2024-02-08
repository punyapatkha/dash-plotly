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
# response = chain.invoke({"question": "can you summarize branch sales in each month "})
# print(response)
# print(db.run(response))
# print(chain.get_prompts()[0].pretty_print())



from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer = answer_prompt | llm | StrOutputParser()
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer
)


response = chain.invoke({"question": "can you summarize each branch sales in each month"})
print(response)