from fastapi import APIRouter,HTTPException
from database.mission_db import MissionDB
from pydantic import BaseModel
from enum import Enum
import logging

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
# @router.get("/missions")
# @router.get("/missions/{id}")
# @router.put("/missions/{id}/assign/{agent_id}")
# @router.put("/missions/{id}/start")
# @router.put("/missions/{id}/complete")
# @router.put("/missions/{id}/fail")
# @router.put("/missions/{id}/cancel")
