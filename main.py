from database.db_connection import ConnectionDB
from database.agent_db import AgentDB
connection=ConnectionDB()
connection.create_database()
connection.create_tables()
agent=AgentDB()
data={"name":"shalom","specialty":"computers","is_active":True,"completed_missions":4,"failed_missions":2,"agent_rank":"Commander"}
# agent.create(data)
print(agent.get_agent_performance())
