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
    return agent.get_all_agents()
# @router.get("/agents/{id}")
# @router.put("/agents/{id}")
# @router.put("/agents/{id}/deactivate")
# @router.get("/agents/{id}/performance")







# @router.post("/agents")
# @router.get("/agents")
# @router.get("/agents/{id}")
# @router.put("/agents/{id}")
# @router.put("/agents/{id}/deactivate")
# @router.get("/agents/{id}/performance")