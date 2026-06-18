from database.db_connection import ConnectionDB
connection=ConnectionDB()
import logging
logger=logging.getLogger(__name__)

class AgentDB:
    def __init__(self):
        pass

    def create_agent(self,data:dict):
        conn=connection.get_connection()
        cursor=conn.cursor()
        sql="INSERT INTO agents (name,specialty,is_active,completed_missions,failed_missions,agent_rank) VALUES (%s,%s,%s,%s,%s,%s)"
        values=(data["name"],data["specialty"],data["is_active"],data["completed_missions"],data["failed_missions"],data["agent_rank"])
        cursor.execute(sql,values)
        conn.commit()
        print("Values inserted successfully")
        new_id=cursor.lastrowid
        cursor.close()
        conn.close()
        data["id"]=new_id
        return data

    def update_agent(self,data:dict,id:int):
        conn=connection.get_connection()
        cursor=conn.cursor()
        set_part=[f"{key}=%s" for key in data.keys()]
        set_clause=",".join(set_part)
        sql=f"UPDATE agents SET {set_clause} WHERE id=%s"
        values=list(data.values())+[id]
        cursor.execute(sql,values)
        conn.commit()
        changed=cursor.rowcount>0
        cursor.close()
        conn.close()
        return changed

    def get_all_agents(self):
        conn=connection.get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents")
        all_agents=cursor.fetchall()
        cursor.close()
        conn.close()
        return all_agents

    def get_agent_by_id(self,id:int):
        conn=connection.get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents WHERE id =%s",(id,))
        get_agent=cursor.fetchone()
        cursor.close()
        conn.close()
        return get_agent

    def deactivate_agent(self,id:int):
        conn=connection.get_connection()
        cursor=conn.cursor()
        cursor.execute("UPDATE agents SET is_active=False WHERE id=%s",(id,))
        conn.commit()
        cursor.close()
        conn.close()

    def count_active_agents(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(id) FROM agents WHERE is_active=True")
            total_active=cursor.fetchone()
            if not total_active: #in case that trying to count the active but the table is empty so we cannot reach to the first place in the tuple
                return None
            return total_active[0]
        finally:
            cursor.close()
            conn.close()

    def get_agent_performance(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT SUM(completed_missions) FROM agents")
            total_completed=cursor.fetchone()
            if not total_completed:
                return total_completed
            cursor.execute("SELECT SUM(failed_missions) FROM agents")
            total_failed=cursor.fetchone()
            if not total_failed:
                return total_failed
            failed=int(total_failed[0])
            completed=int(total_completed[0])
            if completed + failed:
                return None # cannot divide by zero
            return {
                "total": completed + failed,
                "failed": failed,
                "completed": completed,
                "success_rate": (completed / (completed + failed)) * 100
                }
        finally:
            cursor.close()
            conn.close()

    def increment_completed(self,id:int):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE agents SET completed_missions=completed_missions+1 WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
    def increment_failed(self,id:int):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE agents SET failed_missions=failed_missions+1 WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

