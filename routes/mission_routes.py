from fastapi import APIRouter
from database.mission_db import MissionDB
from pydantic import BaseModel
from enum import Enum
import logging
logger=logging.getLogger(__name__)
router=APIRouter()
# @router.post("/missions")
# @router.get("/missions")
# @router.get("/missions/{id}")
# @router.put("/missions/{id}/assign/{agent_id}")
# @router.put("/missions/{id}/start")
# @router.put("/missions/{id}/complete")
# @router.put("/missions/{id}/fail")
# @router.put("/missions/{id}/cancel")
