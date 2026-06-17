from database.db_connection import ConnectionDB
from database.agent_db import AgentDB
connection=ConnectionDB()
connection.create_database()
connection.create_tables()
agent=AgentDB()
data={"name":"moshe","specialty":"math","is_active":False,"completed_missions":2,"failed_missions":1,"agent_rank":"Senior"}
# agent.create(data)
print(agent.get_all_agents())
