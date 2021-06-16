import sqlite3
import random
class Database:
    def __init__(self,db):
        self.conn =sqlite3.connect(db)
        self.cur = self.conn.cursor()
        
        sql_create_employee_table = """ CREATE TABLE IF NOT EXISTS employee (
                                            id integer PRIMARY KEY ,
                                            name text NOT NULL,
                                            status_work text,
                                            car_handled text
                                        ); """

        sql_create_workshop_car_table = """CREATE TABLE IF NOT EXISTS workshop_car (
                                        id integer PRIMARY KEY,
                                        car_name text NOT NULL,
                                        car_status text,
                                        start_date text,
                                        end_date text,
                                        duration text

                                    );"""
        
        sql_create_working_activities_table = """CREATE TABLE IF NOT EXISTS working_activities (
                                        id integer PRIMARY KEY,
                                        emp_id integer NOT NULL,
                                        car_id integer NOT NULL,
                                        clock_in text,
                                        clock_out text,
                                        date_log text,
                                        FOREIGN KEY (emp_id) REFERENCES employee (id),
                                        FOREIGN KEY (car_id) REFERENCES workshop_car (id)

                                    );"""
        self.cur.execute(sql_create_employee_table)
        self.cur.execute(sql_create_workshop_car_table)
        self.cur.execute(sql_create_working_activities_table)
        

    def get_activity_date(self,date):
        self.cur.execute("SELECT * FROM working_activities WHERE date_log='"+date+"'")
        rows = self.cur.fetchall()
        return rows
    def get_activity(self):
        self.cur.execute("SELECT * FROM working_activities")
        rows = self.cur.fetchall()
        return rows
    def get_user(self):
        self.cur.execute("SELECT * FROM employee")
        rows = self.cur.fetchall()
        return rows
    def get_car(self):
        self.cur.execute("SELECT * FROM workshop_car")
        rows = self.cur.fetchall()
        return rows

    def get_car_status(self,id):
        self.cur.execute("SELECT car_status FROM workshop_car WHERE id='"+id+"'")
        rows = self.cur.fetchone()
        return rows
    
   

    def insert(self,emp_id,car_id,clock_in,clock_out,date_log):
        self.cur.execute("INSERT INTO working_activities(emp_id,car_id,clock_in,clock_out,date_log) VALUES(?,?,?,?,?)",(emp_id,car_id,clock_in,clock_out,date_log))
        self.conn.commit()
        
    def remove(self,id):
        self.cur.execute("DELETE FROM working_activities WHERE id='"+str(id)+"';")
        self.conn.commit()

    def update(self,activity_id,emp_id,car_id,clock_in,clock_out,date_log):
        print("UPDATE working_activities SET emp_id=?,car_id=?,clock_in=?,clock_out=?,date_log=? WHERE id=?",(emp_id,car_id,clock_in,clock_out,date_log,activity_id))
        self.cur.execute("UPDATE working_activities SET emp_id=?,car_id=?,clock_in=?,clock_out=?,date_log=? WHERE id=?",(emp_id,car_id,clock_in,clock_out,date_log,activity_id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def sample_data(self):
        for x in range(1,11):
            #print("INSERT INTO employee(name,status_work) VALUES('employee"+str(x)+"','working');" )
            sql_add_employee = "INSERT INTO employee(name,status_work) VALUES('EMPLOYEE_"+str(x)+"','FREE');" 
            self.cur.execute(sql_add_employee)

        for x in range(1,6):
            durationset = random.randrange(1,3)
            sql_add_car = "INSERT INTO workshop_car('car_name','car_status','duration') VALUES('CAR "+str(x)+"','INCOMPLETED',"+str(durationset)+");" 
            self.cur.execute(sql_add_car)

        self.conn.commit()

    def execute(self,param):

        self.cur.execute(param)
        self.conn.commit()

    def assign_user(self,emp_id,car_id,date):
        sql_command = "INSERT INTO working_activities(emp_id,car_id,date_log) VALUES('"+str(emp_id)+"','"+str(car_id)+"','"+date+"');"
        self.cur.execute(sql_command)
        self.conn.commit()

    def add_activity(self,emp_id,car_id,clock_in,clock_out,shift_date):
        
        self.cur.execute("INSERT INTO working_activities(emp_id,car_id,clock_in,clock_out,date_log) VALUES(?,?,?,?,?);",(emp_id,car_id,clock_in,clock_out,shift_date))
        self.conn.commit()

    def updateUserStatus(self,emp_id,user_status,car_id):
        print(user_status,emp_id)
        sql_command = "UPDATE employee SET status_work='"+user_status+"',car_handled='"+car_id+"' WHERE id='"+emp_id+"'"
        self.cur.execute(sql_command)
        self.conn.commit()

    def updateCarStatus(self,car_id,status):
        sql_command = "UPDATE workshop_car SET car_status='"+status+"' WHERE id='"+car_id+"'"
        self.cur.execute(sql_command)
        self.conn.commit()
    def getUserCarID(self,emp_id):
        sql_command = "SELECT car_handled FROM employee WHERE id='"+emp_id+"'"
        self.cur.execute(sql_command)
        rows = self.cur.fetchone()
        return rows
    def getUserStatus(self,emp_id):
        sql_command = "SELECT status_work FROM employee WHERE id='"+emp_id+"'"
        self.cur.execute(sql_command)
        rows = self.cur.fetchone()
        return rows

    def find_car_related_activities(self,car_id):
        sql_command = "SELECT * FROM working_activities WHERE car_id='"+car_id+"'"
        self.cur.execute(sql_command)
        rows = self.cur.fetchall()
        return rows

    def getUserForCar(self,car_id):
        sql_command = "SELECT emp_id FROM working_activities WHERE car_id='"+car_id+"'"
        self.cur.execute(sql_command)
        rows = self.cur.fetchall()
        return rows


    def get_car_duration(self,car_id):
        sql_command = "SELECT duration FROM workshop_car WHERE id="+car_id+""
        self.cur.execute(sql_command)
        rows = self.cur.fetchall()
        return rows

    def findUserCarTarget(self,emp_id):
        sql_command = "SELECT car_id FROM working_activities WHERE date_log=(SELECT MAX(date_log) FROM working_activities WHERE emp_id='"+emp_id+"');"
        self.cur.execute(sql_command)
        rows = self.cur.fetchall()
        return rows