# from logging import exception

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

class UpdateAgent(BaseModel):
    name:str | None = None
    specialty:str | None = None
    is_active:bool | None = None
    completed_missions:int | None=None
    failed_missions:int | None=None
    agent_rank:str| None = None

class CreateAgent(BaseModel):
    name:str
    specialty:str
    is_active:bool | None=True
    completed_missions:int | None=0
    failed_missions:int | None=0
    agent_rank:str

@router.post("/agents",status_code=201)
def add_new_agent(data_of_agent:CreateAgent):
    logger.info("enter to add_new_agent router")
    data_dict=data_of_agent.model_dump()
    if data_dict["agent_rank"] not in ['Junior','Senior','Commander']:
        logger.error("Error: unvalid rank in add_new_agent router")
        raise HTTPException(status_code=400,detail="Error: unvalid rank")
    logger.info("exit from add_new_agent router")
    return {"new agent created successfully:":agent.create_agent(data_dict)}

@router.get("/agents")
def get_agents():
    logger.info("enter to get_agents router")
    return {"The agents in the table:":agent.get_all_agents()}

@router.get("/agents/{id}")
def get_specific_agent(id):
    logger.info("enter to get_specific_agent router")
    try:
        valid_id=int(id)
    except ValueError:
        logger.error("Error: unprocessable data, id should be int")
        raise HTTPException(status_code=422,detail="Error: unprocessable data, id should be int")
    result=agent.get_agent_by_id(valid_id)
    if not result:
        logger.error(f"Error the agent number {valid_id} was not found")
        raise HTTPException(status_code=404,detail=f"Error the agent number {valid_id} was not found")
    logger.info("exit from get_specific_agent router")
    return {"agent found": result}

@router.put("/agents/{id}")
def update_agent(id:int,data:UpdateAgent):
    logger.info("enter to update_agent router")
    data_dict_to_update=data.model_dump(exclude_unset=True)
    if "agent_rank" in data_dict_to_update.keys():
        if data_dict_to_update["agent_rank"] not in ['Junior', 'Senior', 'Commander']:
            logger.error("Error: unvalid rank in add_new_agent router")
            raise HTTPException(status_code=400, detail="Error: unvalid rank")
    result=agent.update_agent(data_dict_to_update,id)
    if not result:
        logger.error("error agent was not found")
        raise HTTPException(status_code=404,detail="error agent was not found")
    logger.info("exit from update_agent router")
    return {"update agent":result}

@router.put("/agents/{id}/deactivate")
def deactivate_agent(id:int):
    result=agent.deactivate_agent(id)
    if not result:
        raise HTTPException(status_code=404,detail=f"Error the agent number {id} was not found")
    return {f"deactivate agent number {id}":result}

@router.get("/agents/{id}/performance")
def get_performance(id):
    logger.info("enter to get_performance router")
    try:
        valid_id=int(id)
    except ValueError:
        logger.error("Error: unprocessable data, id should be int")
        raise HTTPException(status_code=422,detail="Error: unprocessable data, id should be int")
    result=agent.get_agent_performance(valid_id)
    if not result:
        logger.info(f"Error the agent number {valid_id} was not found or that the the tabel is empty so it impossible to calculate the percentage")
        raise HTTPException(status_code=404,detail=f"Error the agent number {valid_id} was not found"
                                                   f"or that the the tabel is empty so it impossible to calculate the percentage")
    logger.info("exit from get_performance router")
    return {"agent found": result}