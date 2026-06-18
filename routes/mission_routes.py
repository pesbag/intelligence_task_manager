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
    mission_dict=data.model_dump()
    mission_dict["risk_level"]=calc_level(mission_dict["difficulty"], mission_dict["importance"])
    try:
        result=mission.create_mission(mission_dict)
    except Exception:
        raise HTTPException(status_code=400,detail="Error the range values of difficult and importance should be between 1 to 10")
    return {"new agent created successfully:": result}

@router.get("/missions")
def get_missions():
    return {"The missions in the table:":mission.get_all_missions()}

@router.get("/missions/{id}")
def get_specific_mission(id):
    try:
        valid_id = int(id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Error: unprocessable data, id should be int")
    result = mission.get_mission_by_id(valid_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Error the mission number {valid_id} was not found")
    return {"mission found": result}
# @router.put("/missions/{id}/assign/{agent_id}")
@router.put("/missions/{id}/start")
def start_mission(id:int):
    is_exists = mission.get_mission_by_id(id)
    if not is_exists:
        raise HTTPException(status_code=404, detail=f"Error the mission number {id} was not found")
    if is_exists["status"] != "ASSIGNED":
        raise HTTPException(status_code=400, detail="Error cannot cancel a non IN_PROGRESS mission")
    result = mission.update_mission_status(id, "IN_PROGRESS")
    return {f"mission status number {id} changed": result}


@router.put("/missions/{id}/complete")
def mission_complete(id:int):
    is_exists=mission.get_mission_by_id(id)
    if not is_exists:
        raise HTTPException(status_code=404, detail=f"Error the mission number {id} was not found")
    if is_exists["status"]!="IN_PROGRESS" or is_exists["status"]=="COMPLETED":
        raise HTTPException(status_code=400,detail="Error cannot complete a non IN_PROGRESS mission")
    result=mission.update_mission_status(id,"COMPLETED")
    agent.increment_completed(is_exists["assigned_agent_id"])
    return {f"mission status number {id} changed":result}

@router.put("/missions/{id}/fail")
def mission_failed(id:int):
    is_exists=mission.get_mission_by_id(id)
    if not is_exists:
        raise HTTPException(status_code=404, detail=f"Error the mission number {id} was not found")
    if is_exists["status"]!="IN_PROGRESS" or is_exists["status"]=="COMPLETED":
        raise HTTPException(status_code=400,detail="Error cannot fail a non IN_PROGRESS mission")
    result=mission.update_mission_status(id,"FAILED")
    agent.increment_failed(is_exists["assigned_agent_id"])
    return {f"mission status number {id} changed":result}

@router.put("/missions/{id}/cancel")
def cancel_mission(id:int):
    is_exists = mission.get_mission_by_id(id)
    if not is_exists:
        raise HTTPException(status_code=404, detail=f"Error the mission number {id} was not found")
    if is_exists["status"] != "NEW" and is_exists["status"] != "ASSIGNED":
        raise HTTPException(status_code=400, detail="Error cannot cancel a non IN_PROGRESS mission")
    result = mission.update_mission_status(id, "CANCELLED")
    return {f"mission status number {id} changed": result}
