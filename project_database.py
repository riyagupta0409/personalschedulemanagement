# # import all necessary modules 
import sqlite3 as sq
from datetime import datetime , date , time
from os import system
# # Adding color to text in cmd
system("color")
COLOR = {
    "Bold":"\033[1m",
    "Dim":"\033[2m",
    "Underlined":"\033[4m",
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "YELLOW":"\033[33m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",   # # color-off
    "PURPLE":"\033[0;35m",
    "CYAN": "\033[0;36m"
}

# # creating Connection
conn = sq.connect("project.db")
cur = conn.cursor()

# # Function for Creating Tables
def create_tables():
	# conn = sq.connect("project.db")
	# cur = conn.cursor()
	sql_record_table_query = """ CREATE TABLE IF NOT EXISTS records(
							in_date char(11) NOT NULL,
							in_time char(20) NOT NULL,
							out_date char(11) ,
							out_time char(20),
							duration char(30),
							Task_completed INTEGER,
							Extra_Tasks INTEGER );
							"""
	cur.execute(sql_record_table_query)

	sql_current_tasks = """CREATE TABLE IF NOT EXISTS tasks(
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						task varchar(255) NOT NULL,
						status INTEGER );
						"""
	cur.execute(sql_current_tasks)

	sql_pending_task = """CREATE TABLE IF NOT EXISTS pending_tasks(
						  id INTEGER unique,
						  task_date varchar(20),
						  task varchar(255) );"""
	cur.execute(sql_pending_task)
	conn.commit()

# # create tables
create_tables()

# # function for checking the status
def check_user_status():
	# conn = sq.connect("project.db")
	# cur = conn.cursor()
	q=""" SELECT count(*) FROM tasks ;
	  """
	cur.execute(q)
	top = cur.fetchall()
	if top[0][0] == 0:
		return 0   # # 0 means out
	else:
		return 1   # # 1 means inn 
# # SHOW PREVIOUS RECORDS
def previous_records():
	print(COLOR["BLUE"])
	print("""                     _______________________________________ """)
	print("""                    |                                       |""")
	print("""                    |            PREVIOUS RECORD            |""")
	print("""                    |_______________________________________|""")
	print(COLOR["ENDC"])	
	print()
	q="""SELECT * FROM records WHERE out_date is not null"""
	cur.execute(q)
	print(COLOR["YELLOW"]," S.No. ","IN DATE".center(13," "),"IN TIME".center(11," "),"OUT DATE".center(13," "),"OUT TIME".center(11," "),"DURATION".center(18," ")," COMPLETED(%) ","EXTRAS",COLOR["ENDC"],sep=" ")
	j=1
	for row in cur.fetchall():
		print(COLOR["Bold"],str(j).center(6),row[0].center(12," "),row[1].center(10," "),row[2].center(12," "),row[3].center(10," "),row[4].center(17," "),str(row[5]).center(13," "),str(row[6]).center(6," "),sep="| ")
		j+=1
	print(COLOR["ENDC"])
# Adding a new record to the record table
def add_record(in_date,in_time):


	q="""INSERT INTO records(in_date,in_time)	
			VALUES(?,?) ;"""
	cur.execute(q,(in_date,in_time))
	conn.commit()

# adding tasks into tasks table
def add_task_in_db(task):
	q="""INSERT INTO tasks(task,status)
		VALUES(?,?)"""
	cur.execute(q,(task,0))
	conn.commit()

# # show current session details
def current_time_details():
	q="""SELECT in_date ,in_time FROM records WHERE out_date IS NULL """
	cur.execute(q)
	row = cur.fetchone()
	in_time=str(row[1])
	in_date=str(row[0])
	in_time_complete_object = in_date+" "+in_time
	print(COLOR["BLUE"],"     ","IN DATE :".rjust(20," "),in_date,"IN TIME :".rjust(15," "),in_time)
	now = datetime.now()
	current= str(time(now.hour, now.minute, now.second))
	FMT="%H:%M:%S"
	print("DURATION : ".rjust(40," "),end=" ")
	print(datetime.strptime(current,FMT)-datetime.strptime(in_time,FMT),COLOR["ENDC"])

	
# checking status of tasks and showing tasks
def show_tasks():
	q = """ SELECT * FROM tasks """
	cur.execute(q)
	print()
	print(COLOR["Bold"]," "*26,"<<< YOUR TASKS ARE >>>")
	print(COLOR["GREEN"])
	print(" "*24," Task Id |   Status   | Task ",COLOR["ENDC"])
	for row in cur.fetchall():
		if(row[2] == 0):	
			print(COLOR["Bold"]," "*23," {}| {}| {}".format((str(row[0])).center(8,' '),"Incomplete".ljust(11,' '),row[1]),sep=" ")
		else:
			print(COLOR["Bold"]," "*23," {}| {}| {}".format((str(row[0])).center(8,' '),"Completed".ljust(11,' '),row[1]),sep=" ")


# # completed a task
def Completed_a_task(taskid):
	q="""UPDATE tasks SET status = 1 WHERE id = {}""".format(taskid)
	cur.execute(q)
	conn.commit()

# # remove a task using id
def remove_task_from_db(task_id):
	q="""DELETE FROM tasks WHERE id = {}""".format(task_id)
	cur.execute(q)
	conn.commit()

# # pending tasks insertion
def insert_in_pending_tasks(task_id,task):
	date = str(datetime.today())
	q="""INSERT INTO pending_tasks(id,task_date,task) VALUES(?,?,?)"""
	cur.execute(q,(task_id,date,task))
	conn.commit()

# # fetch from pending tasks and make it empty
def show_pending_tasks():

	q="""SELECT * FROM pending_tasks"""
	cur.execute(q)
	print(COLOR["BLUE"])
	print("""                     _______________________________________ """)
	print("""                    |                                       |""")
	print("""                    |             PENDING TASKS             |""")
	print("""                    |_______________________________________|""")
	print(COLOR["ENDC"])	
	print()
	print(COLOR["YELLOW"]," "*18," TASK ID  |    DATE    | TASK",COLOR["ENDC"])
	for row in cur.fetchall():
		date = str(row[1])
		date = date[0:10]
		print(" "*18,"{}| {} | {}".format(str(row[0]).center(11," "),date,row[2]))
	print(COLOR["ENDC"])
			
# # completed a pending task
def Completed_a_pending_task(task_id):
	q="""DELETE FROM pending_tasks WHERE id = {}""".format(task_id)
	cur.execute(q)
	conn.commit()
	
# # empty pending task table
def empty_pending_task_table():
	q="""DELETE FROM pending_tasks"""
	cur.execute(q)
	conn.commit()	


# # COMPLETE PENDING RECORD
def complete_record(out_date,out_time,extra_task_len):
	q="""SELECT in_date ,in_time FROM records WHERE out_date IS NULL """
	cur.execute(q)
	row = cur.fetchone()
	in_time=row[1]
	in_date=row[0]
	in_time_complete = row[0]+" "+row[1]
	in_time_complete_object =datetime.strptime(in_time_complete, "%Y-%m-%d %H:%M:%S")
	out_time_complete = out_date+" "+out_time
	out_time_complete_object =datetime.strptime(out_time_complete, "%Y-%m-%d %H:%M:%S")
	difference = str(out_time_complete_object-in_time_complete_object)
	q1="""SELECT count(*) FROM tasks WHERE status = 1 """
	cur.execute(q1)
	x=cur.fetchone()
	task_comp = x[0]
	q2="""SELECT count(id) From tasks"""
	cur.execute(q2)
	x=cur.fetchone()
	total_tasks = x[0]
	percent_task_done = (task_comp*100)//total_tasks
	q3 = """UPDATE records 
			SET out_date =?,out_time=?,duration=?,Task_completed=?,Extra_tasks=?
			WHERE out_date IS NULL"""
	cur.execute(q3,(out_date,out_time,difference,percent_task_done,extra_task_len))
	print(COLOR["BLUE"])
	print("""                     _______________________________________ """)
	print("""                    |                                       |""")
	print("""                    |             TODAY'S REPORT            |""")
	print("""                    |_______________________________________|""",COLOR["ENDC"])
	print(COLOR["GREEN"])	
	print("                   IN DATE : {}    IN TIME : {}".format(in_date,in_time))
	print("                   OUT DATE : {}   OUT TIME : {}".format(out_date,out_time))
	print("                              DURATION : {}".format(difference))
	print("                   TOTAL TASKS:{}  COMPLETED: {}%  EXTRA TASKS :{}".format(total_tasks,percent_task_done,extra_task_len))
	print(COLOR["ENDC"])
	print(COLOR["Bold"],"<<<<   TASKS COMPLETED    >>>>")
	q1="""SELECT * FROM tasks WHERE status = 1 """
	cur.execute(q1)
	j=1
	for row in cur.fetchall():
		print("  {}.  {}".format(j,row[1]))
		j+=1
	q4 = """SELECT * from tasks WHERE status = 0"""
	cur.execute(q4)
	for row in cur.fetchall():
		insert_in_pending_tasks(row[0],row[1])
	empty_task_table()
	conn.commit()

# # Delete Entries from Task Table
def empty_task_table():
	cur.execute("""DELETE FROM tasks""")
	conn.commit()

# for closing database and commit changes
def close_database():
	conn.commit()
	conn.close()
# cur.execute("""DELETE FROM records""")
# conn.commit()
