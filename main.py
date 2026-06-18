from database.db_connection import ConnectionDB
from database.agent_db import AgentDB
from database.mission_db import MissionDB
from fastapi import FastAPI
from routes import agent_routes
from routes import mission_routes
from routes import report_routes
import logging

connection=ConnectionDB()
connection.create_database()
connection.create_tables()

app=FastAPI()
app.include_router(agent_routes.router)
app.include_router(mission_routes.router)
app.include_router(report_routes.router)

agent=AgentDB()
mission=MissionDB()

path_to_file="logs/app.log"
logging.basicConfig(
    filename=path_to_file,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# data={"name":"shalom","specialty":"computers","is_active":True,"completed_missions":4,"failed_missions":2,"agent_rank":"Commander"}
# # agent.create(data)
# print(agent.get_agent_performance())
