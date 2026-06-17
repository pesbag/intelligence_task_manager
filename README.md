# Intelligence Task Manager
``` 
An intelligence unit called SadowNet needs a system to help it manage its agents and missions.
This project helps it with that problem.
```
### In this project, we create a connection to a new database called intelligence_db and there we will create 2 tables.
##### One table called agents will contain information about the agents
##### Second table called missions will contain information about the missions
- The structure of the tables is:
- #### agents:
```
| id (INT,PK,AUTO_INCREMENT,UNIQUE) | name (VARCHAR(30)) | specialty (VARCHAR(30)) | is_active (BOOLEAN, DEFAULT:TRUE) | completed_mission (INT, DEFAULT:0) | failed_mission (INT DEFAULT:0) | agent_rank (ENUM('Junior','Senior','Commander')) |
```
- #### mission:
```
| id (INT,PK,AUTO_INCREMENT,UNIQUE) | title (VARCHAR(30)) | description TEXT | location (VARCHAR(30)) | difficulty (INT, 1 TO 10 ONLY) | importance (INT, 1 TO 10 ONLY) | status (VARCHAR(30) DEFAULT:NEW) | risk_level (VARCHAR(30) AUTOMATIC CALCULATION) | assigned_agent_id (INT DEFAULT NULL) |
```
- The structure of the folders is:
```
intelligence-task-manager/ 
├── database/ 
│   ├── db_connection.py 
│   ├── agent_db.py 
│   └── mission_db.py 
├── README.md 
├── requirements.txt 
└── .gitignore 
```
- There is 3 class, the first called MissionDB, the second called AgentDB, the third called ConnectionDB
- #### in MissionDB we have the following functions:
- create_mission(data) that create a new mission by given data, return the all object.
- get_all_mission() that return all the missions.
- get_mission_by_id(id) that return a specific mission by given his id.
- assign_mission(m_id,a_id) that associate mission to agent.
- update_mission_status(id,status) that update the status of mission by given mission id.
- get_open_missions(id) that return the mission in status 'ASSIGNED' or 'IN_PROGRESS' of specific agent by given his id.
- count_all_mission() that return the total mission in the table.
- count_by_status(status) that return the total mission in a specific status.
- count_open_status() that return the number of open status in the table.
- count_critical_mission() that return the number of critical missions in the table.
- get_top_agent() that return the agent with the highest completed_missions.
- #### in AgentDB we have the following functions:
- create_agent(data) that create a new agent by given data of agent, return the new object of the agent.
- get_all_agent() that return a list of all the agents
- get_agent_by_id(id) that return a specific agent by given his id, return agent or None.
- update_agent(id,data) that update the data of specific agent given by his id, cannot update the id.
- deactivate_agent(id) that make the given agent, by his id, deactivate.
- increment_completed(id) that update the number of mission completed by specific agent.
- get_agent_performance(id) that return the following dictionary: {'completed': value,'failed': value,'success_rate':value}.
- count_active_agents() that return the number of active agents.
- #### in ConnectionDB we have the following functions: 
- get_connection() that return active connection to MySQL
- create_database() that create intelligence_db if not exists
- create_tables() that create the 2  needed tables if not exists
### The rules of the system:
- 1: rank must be Junior / Senior / Commander any other value throws an error
- 2: difficulty and importance otherwise error. Must be between 10 and 1
- 3: risk_level user does not send it - automatically calculated when creating a task
- 4: Agent with is_active=False cannot accept tasks.
- 5: Agent cannot have more than 3 open tasks at the same time ( ASSIGNED / IN_PROGRESS)
- 6: If risk_level=CRITICAL then only an agent with Commander rank can accept the task.
- 7: A task can only be assigned in status=ASSIGNED, after assignment: NEW.
- 8: A task can only be started in status ASSIGNED after: status=IN_PROGRESS.
- 9: A task can only be ended when IN_PROGRESS and changed to failed or completed status.
- 10: A task can only be canceled in status NEW or ASSIGEND otherwise error.
### How to run the project:
- Enter to the terminal and run the next command:
```
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0 
```
- Then enter to main.py folder and run it