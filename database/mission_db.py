from database.db_connection import ConnectionDB
connection=ConnectionDB()
class MissionDB:
    def __init__(self):
        pass
    def calc_level(self,difficulty,importance):
        result=difficulty*2+importance
        if result<10:
            return "LOW"
        elif result<18:
            return "MEDIUM"
        elif result<25:
            return "HIGH"
        else:
            return "CRITICAL"
    def create_mission(self,data:dict):
        conn=connection.get_connection()
        cursor=conn.cursor()
        sql="INSERT INTO missions (title,description,location,difficulty,importance,status,risk_level,assigned_agent_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(data["title"],data["description"],data["location"],data["difficulty"],data["importance"],data["status"],self.calc_level(data["difficulty"],data["importance"]),data["assigned_agent_id"])
        cursor.execute(sql,values)
        conn.commit()
        print("Values inserted successfully")
        new_id=cursor.lastrowid
        cursor.close()
        conn.close()
        data["id"]=new_id
        return data

    def get_all_missions(self):
        conn=connection.get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions")
        all_agents=cursor.fetchall()
        cursor.close()
        conn.close()
        return all_agents

    def get_mission_by_id(self,id:int):
        conn=connection.get_connection()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE id =%s",(id,))
        get_agent=cursor.fetchone()
        cursor.close()
        conn.close()
        return get_agent


    def count_open_missions(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(id) FROM missions WHERE status='ASSIGNED' OR status='IN_PROGRESS'")
            total_open=cursor.fetchone()
            if not total_open: #in case that trying to count the open missions but the table is empty so we cannot reach to the first place in the tuple
                return None
            return total_open[0]
        finally:
            cursor.close()
            conn.close()

    def count_critical_missions(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(id) FROM missions WHERE risk_level='CRITICAL'")
            total_critical = cursor.fetchone()
            if not total_critical:  # in case that trying to count the critical missions but the table is empty so we cannot reach to the first place in the tuple
                return None
            return total_critical[0]
        finally:
            cursor.close()
            conn.close()

    def get_top_agent(self):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT assigned_agent_id,count(status) FROM missions WHERE status='COMPLETED' GROUP BY assigned_agent_id")
        top_agent=cursor.fetchone()
        cursor.close()
        conn.close()
        return top_agent

    def count_by_status(self,status):
        conn=connection.get_connection()
        cursor=conn.cursor()
        try:
            cursor.execute("SELECT COUNT(id) from missions WHERE status=%s",(status,))
            status_count=cursor.fetchone()
            if not status_count: # in case that trying to count the status but the table is empty so we cannot reach to the first place in the tuple
                return None
            return status_count[0]
        finally:
            cursor.close()
            conn.close()

    def count_all_missions(self):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions")
        all_agents = cursor.fetchall()
        cursor.close()
        conn.close()
        return all_agents

    def update_mission_status(self,id:int,status):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE missions SET status=%s WHERE id=%s",(status,id))
        conn.commit()
        changed = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return changed

    def get_open_missions_by_agent(self,id:int):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT title,description FROM missions WHERE id=%s AND (status='ASSIGNED' OR status='IN_PROGRESS')",(id,))
        open_missions=cursor.fetchall()
        cursor.close()
        conn.close()
        return open_missions

    def assign_mission(self,m_id,a_id):
        conn = connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE missions SET assigned_agent_id=%s WHERE id=%s",(a_id,m_id))
        conn.commit()
        changed = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return changed

if __name__=="__main__":
    mis=MissionDB()
    data={"title": "D","description":"its mission D","location":"KFJ","difficulty":3,"importance":3,"status":"COMPLETED","risk_level":"LOW","assigned_agent_id":3}
    print(mis.get_all_missions())
    print(mis.get_top_agent())