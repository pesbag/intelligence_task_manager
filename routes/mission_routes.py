from fastapi import APIRouter,HTTPException
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from pydantic import BaseModel
from enum import Enum
import logging

agent=AgentDB()
mission=MissionDB()

logger=logging.getLogger(__name__)
router=APIRouter()


def calc_level(difficulty, importance):
    logger.info("enter to calc_level function")
    result = difficulty * 2 + importance
    if result < 10:
        return "LOW"
    elif result < 18:
        return "MEDIUM"
    elif result < 25:
        return "HIGH"
    else:
        return "CRITICAL"

class ValidStatus(str,Enum):
    NEW='NEW'
    ASSIGNED='ASSIGNED'
    IN_PROGRESS='IN_PROGRESS'
    COMPLETED='COMPLETED'
    FAILED='FAILED'
    CANCELLED='CANCELLED'

class CreateMission(BaseModel):
    title:str
    description:str
    location:str
    difficulty:int
    importance:int
    status: ValidStatus
    assigned_agent_id:int | None=None

@router.post("/missions")
def add_new_mission(data:CreateMission):
    logger.info("enter to add_new_mission router")
    mission_dict=data.model_dump()
    mission_dict["risk_level"]=calc_level(mission_dict["difficulty"], mission_dict["importance"])
    try:
        result=mission.create_mission(mission_dict)
    except Exception:
        logger.exception("Error the range values of difficult and importance should be between 1 to 10")
        raise HTTPException(status_code=400,detail="Error the range values of difficult and importance should be between 1 to 10")
    logger.info("exit from add_new_mission router")
    return {"new agent created successfully:": result}

@router.get("/missions")
def get_missions():
    logger.info("enter to get_missions router")
    return {"The missions in the table:":mission.get_all_missions()}

@router.get("/missions/{id}")
def get_specific_mission(id):
    logger.info("enter to get_specific_mission router")
    try:
        valid_id = int(id)
    except ValueError:
        logger.exception("Error: unprocessable data, id should be int")
        raise HTTPException(status_code=422, detail="Error: unprocessable data, id should be int")
    result = mission.get_mission_by_id(valid_id)
    if not result:
        logger.exception(f"Error the mission number {valid_id} was not found")
        raise HTTPException(status_code=404, detail=f"Error the mission number {valid_id} was not found")
    logger.info("exit from get_specific_mission router")
    return {"mission found": result}

@router.put("/missions/{id}/assign/{agent_id}")
def mission_assign(id:int,agent_id:int):
    logger.info("enter to mission_assign router")
    is_mission_exists=mission.get_mission_by_id(id)
    if not is_mission_exists:
        logger.exception(f"Mission not found")
        raise HTTPException(status_code=404,detail="Mission not found")
    is_agent_exists=agent.get_agent_by_id(agent_id)
    if not is_agent_exists:
        logger.exception(f"Agent not found")
        raise HTTPException(status_code=404,detail="Agent not found")
    if is_mission_exists["status"]=="NEW":
        logger.exception(f"Mission not available")
        raise HTTPException(status_code=400,detail="Mission not available")
    if is_agent_exists["is_active"]==False:
        logger.exception(f"Agent is not active")
        raise HTTPException(status_code=400,detail="Agent is not active")
    if mission.get_open_missions_by_agent(agent_id)>3:
        logger.exception(f"Agent has reached maximum missions")
        raise HTTPException(status_code=400,detail="Agent has reached maximum missions")
    if is_mission_exists["risk_level"]=="CRITICAL" and is_agent_exists["agent_rank"]!="Commander":
        logger.exception(f"Only Commander can handle critical missions")
        raise HTTPException(status_code=400,detail="Only Commander can handle critical missions")
    result=mission.assign_mission(id,agent_id)
    return {"mission assign": result}

@router.put("/missions/{id}/start")
def start_mission(id:int):
    logger.info("enter to start_mission router")
    is_exists = mission.get_mission_by_id(id)
    if not is_exists:
        logger.error(f"Error the mission number {id} was not found")
        raise HTTPException(status_code=404, detail=f"Error the mission number {id} was not found")
    if is_exists["status"] != "ASSIGNED":
        logger.error("Error cannot cancel a non IN_PROGRESS mission")
        raise HTTPException(status_code=400, detail="Error cannot cancel a non IN_PROGRESS mission")
    result = mission.update_mission_status(id, "IN_PROGRESS")
    logger.info("exit from start_mission router")
    return {f"mission status number {id} changed": result}


@router.put("/missions/{id}/complete")
def mission_complete(id:int):
    logger.info("enter to mission_complete router")
    is_exists=mission.get_mission_by_id(id)
    if not is_exists:
        logger.error(f"Error the mission number {id} was not found")
        raise HTTPException(status_code=404, detail=f"Error the mission number {id} was not found")
    if is_exists["status"]!="IN_PROGRESS" or is_exists["status"]=="COMPLETED":
        logger.error("Error cannot complete a non IN_PROGRESS mission")
        raise HTTPException(status_code=400,detail="Error cannot complete a non IN_PROGRESS mission")
    result=mission.update_mission_status(id,"COMPLETED")
    agent.increment_completed(is_exists["assigned_agent_id"])
    logger.info("exit from mission_complete router")
    return {f"mission status number {id} changed":result}

@router.put("/missions/{id}/fail")
def mission_failed(id:int):
    logger.info("enter to mission_field router")
    is_exists=mission.get_mission_by_id(id)
    if not is_exists:
        logger.error(f"Error the mission number {id} was not found")
        raise HTTPException(status_code=404, detail=f"Error the mission number {id} was not found")
    if is_exists["status"]!="IN_PROGRESS" or is_exists["status"]=="COMPLETED":
        logger.error("Error cannot fail a non IN_PROGRESS mission")
        raise HTTPException(status_code=400,detail="Error cannot fail a non IN_PROGRESS mission")
    result=mission.update_mission_status(id,"FAILED")
    agent.increment_failed(is_exists["assigned_agent_id"])
    logger.info("exit form mission_field router")
    return {f"mission status number {id} changed":result}

@router.put("/missions/{id}/cancel")
def cancel_mission(id:int):
    logger.info("enter to cancel_mission router")
    is_exists = mission.get_mission_by_id(id)
    if not is_exists:
        logger.error(f"Error the mission number {id} was not found")
        raise HTTPException(status_code=404, detail=f"Error the mission number {id} was not found")
    if is_exists["status"] != "NEW" and is_exists["status"] != "ASSIGNED":
        logger.error("Error cannot cancel a non IN_PROGRESS mission")
        raise HTTPException(status_code=400, detail="Error cannot cancel a non IN_PROGRESS mission")
    result = mission.update_mission_status(id, "CANCELLED")
    logger.info("exit from cancel_mission router")
    return {f"mission status number {id} changed": result}
