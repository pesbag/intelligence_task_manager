from fastapi import APIRouter
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from pydantic import BaseModel
from enum import Enum
import logging
logger=logging.getLogger(__name__)
router=APIRouter()
# @router.get("/reports/summary")
# @router.get("/reports/missions-by-status")
# @router.get("/reports/top-agent")
