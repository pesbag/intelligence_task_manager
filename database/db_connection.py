import mysql.connector
class ConnectionDB:
    def __init__(self):
        self.host="localhost"
        self.port=3306
        self.user="root"
        self.password="1234"

    def get_connection(self):
        conn= mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database="Intelligence_db"
        )
        cursor=conn.cursor()
        cursor.execute("USE Intelligence_db")
        return conn

    def create_database(self):
        conn=mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password
            )
        cursor=conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
        print("created database successfully")
        # cursor.execute("USE Intelligence_db")
        cursor.close()
        conn.close()

    def create_tables(self):
        conn=self.get_connection()
        cursor=conn.cursor()
        sql="""CREATE TABLE IF NOT EXISTS agents(
               id INT PRIMARY KEY AUTO_INCREMENT,
               name VARCHAR(30) NOT NULL,
               specialty VARCHAR(30) NOT NULL,
               is_active BOOLEAN DEFAULT True,
               completed_missions INT DEFAULT 0,
               failed_missions INT DEFAULT 0,
               agent_rank ENUM('Junior','Senior','Commander')
        )"""
        cursor.execute(sql)
        conn.commit()
        print("Table agents created")

        sql="""CREATE TABLE IF NOT EXISTS missions(
               id INT PRIMARY KEY AUTO_INCREMENT,
               title VARCHAR(30) NOT NULL,
               description TEXT NOT NULL,
               location VARCHAR(30) NOT NULL,
               difficulty INT CHECK (difficulty>=1 AND difficulty<=10),
               importance INT CHECK (importance >=1 AND importance <=10),
               status VARCHAR(30) DEFAULT 'NEW',
               risk_level VARCHAR(30) NOT NULL,
               assigned_agent_id INT DEFAULT NULL
        )"""
        cursor.execute(sql)
        conn.commit()
        print("Table missions created")
        cursor.close()
        conn.close()