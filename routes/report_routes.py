from fastapi import APIRouter,HTTPException
from database.mission_db import MissionDB
from database.agent_db import AgentDB
import logging
mission=MissionDB()
agent=AgentDB()

logger=logging.getLogger(__name__)
router=APIRouter()

@router.get("/reports/summary")
def summary():
    logger.info("enter to summary router")
    total_active=agent.count_active_agents()
    total_mission=mission.count_all_missions()
    open_mission=mission.count_open_missions()
    complete_mission=mission.count_by_status("COMPLETED")
    field_mission=mission.count_by_status("FAILED")
    critical_mission=mission.count_critical_missions()
    logger.info("exit from summary router")
    return {
            "active_agents_count": total_active,
            "total_missions": total_mission,
            "open_missions": open_mission,
            "completed_missions":  complete_mission,
            "failed_missions": field_mission,
            "critical_missions": critical_mission
}

@router.get("/reports/missions-by-status")
def get_missions_by_status():
    logger.info("enter to get_missions_by_status router")
    logger.info("exit from get_missions_by_status router")
    return {
      "open": mission.count_by_status("ASSIGNED") + mission.count_by_status("IN_PROGRESS"),
      "completed": mission.count_by_status("COMPLETED"),
      "failed": mission.count_by_status("FAILED"),
      "canceled":mission.count_by_status("CANCELLED")
    }

@router.get("/reports/top-agent")
def top_agent():
    logger.info("enter to top_agent router")
    get_mission=mission.get_top_agent()
    result=agent.get_agent_by_id(get_mission["assigned_agent_id"])
    if not result:
        logger.error("Error agent was not found")
        raise HTTPException(status_code=404,detail="Error agent was not found")
    logger.info("exit from top_agent router")
    return {"The top agent is:": result}