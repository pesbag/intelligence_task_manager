from logging import exception

from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB
from pydantic import BaseModel
from enum import Enum
import logging
agent=AgentDB()
router=APIRouter()

logger=logging.getLogger(__name__)

# class AgentRank(str,Enum):
#     Junior='Junior'
#     Senior='Senior'
#     Commandr='Commander'

class CreateAgent(BaseModel):
    name:str
    specialty:str
    is_active:bool | None=True
    completed_missions:int | None=0
    failed_missions:int | None=0
    agent_rank:str

@router.post("/agents")
def add_new_agent(data_of_agent:CreateAgent):
    data_dict=data_of_agent.model_dump()
    if data_dict["agent_rank"] not in ['Junior','Senior','Commander']:
        raise HTTPException(status_code=400,detail="Error: unvalid rank")
    return {"new agent created successfully:":agent.create_agent(data_dict)}

@router.get("/agents")
def get_agents():
    return {"The agents in the table:":agent.get_all_agents()}
@router.get("/agents/{id}")
def get_specific_agent(id):
    try:
        valid_id=int(id)
    except ValueError:
        raise HTTPException(status_code=422,detail="Error: unprocessable data, id should be int")
    result=agent.get_agent_by_id(valid_id)
    if not result:
        raise HTTPException(status_code=404,detail=f"Error the agent number {valid_id} was not found")
    return {"agent found": result}
# @router.put("/agents/{id}")

# @router.put("/agents/{id}/deactivate")
@router.get("/agents/{id}/performance")
def get_performance(id):
    try:
        valid_id=int(id)
    except ValueError:
        raise HTTPException(status_code=422,detail="Error: unprocessable data, id should be int")
    result=agent.get_agent_performance(valid_id)
    if not result:
        raise HTTPException(status_code=404,detail=f"Error the agent number {valid_id} was not found"
                                                   f"or that the the tabel is empty so it impossible to calculate the percentage")
    return {"agent found": result}






# @router.post("/agents")
# @router.get("/agents")
# @router.get("/agents/{id}")
# @router.put("/agents/{id}")
# @router.put("/agents/{id}/deactivate")
# @router.get("/agents/{id}/performance")