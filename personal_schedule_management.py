from os import name,system
import project_database as pd
from datetime import datetime , date , time
from time import sleep

# # Adding color to text in cmd
system("color")
COLOR = {
    "Bold":"\033[1m",
    "Dim":"\033[2m",
    "Underlined":"\033[4m",
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",   # # color-off
}

# # Function for clearing CMD 
def clear():
	if name == "nt":
		_=system('cls')
	else:
		_=system('clear')

# # main screen
def main_screen():
	clear()
	while(1):
		print(COLOR["BLUE"])
		print("""                     _______________________________________""")
		print("""                    |                                       |""")
		print("""                    |    YOUR PERSONAL SCHEDULE MANAGER     |""")
		print("""                    |_______________________________________|""")
		print()
		print()
		print("          1.NEW/CURRENT SESSION    2.PREVIOUS SESSIONS    3.PENDING TASKS".rjust(7," "),COLOR["ENDC"])
		print()
		choice = input(">>> ENTER YOUR CHOICE :-  ")
		print()
		if choice =='1':
			clear()
			person.check_status()    
		elif choice =='2':
			clear()
			pd.previous_records()  
		elif choice == '3':
			person.pending_tasks()
			break
		else:	
			print(COLOR["RED"],"      ----Invalid Choice !!---- ",COLOR["ENDC"])
			sleep(1)
			clear()	

# # CLASS FOR PERSONAL SCHEDULE MANAGEMENT

class schedule_management:
	extra_tasks_list = []

	# # function for checking status
	def check_status(self):
		status = pd.check_user_status()
		if status == 0:
			self.virtually_in()
		else:
			self.show_current_session()

	# # Function for getting virtually in for new record
	def virtually_in(self):
		self.in_date = date.today()
		now = datetime.now()
		self.in_time = time(now.hour, now.minute, now.second)
		# print("      IN DATE :".rjust(20," "),self.in_date,"IN TIME :".rjust(15," "),self.in_time)
		# print()
		self.assign_tasks()

	# # option 3 - pending tasks
	def pending_tasks(self):
		clear()
		pd.show_pending_tasks()
		print(COLOR["GREEN"])
		print(" "*11," 1. COMPLETED ANY PENDING TASK ?      2. <- GO BACK",COLOR["ENDC"])
		print()
		choice = input('>>>    Enter your choice(Number) -> ')
		print(COLOR["Bold"])
		if choice == '1' :
			print()
			position = input('>>>   Enter TaskId of Task Completed -->  ')
			while type(position) is not int:
				try:
					position = int(position)
				except ValueError:
					print(COLOR["RED"])
					print("--Enter An Integer Value--".rjust(40," "))
					print(COLOR["ENDC"])
					position = input('>>>   Enter TaskId of task Completed -->  ')
					position = int(position)
			pd.Completed_a_pending_task(position)
			self.pending_tasks()
		elif choice == '2':
			main_screen()
		else:
			print(COLOR["RED"],"    ----ENTER INPUT FROM THE CHOICE GIVEN----    ",COLOR["ENDC"])



	# ASSIGN TASKS 
	def assign_tasks(self):
		print(COLOR["BLUE"])
		print("""                     _______________________________________ """)
		print("""                    |                                       |""")
		print("""                    |               NEW SESSION             |""")
		print("""                    |_______________________________________|""")
		print()
		print(COLOR["ENDC"]) 
		print() 
		while True:
			num = input("Enter Number of tasks you want to do in this session -> ")
			try:
				num = int(num)
				if num > 0:
					break
				else:
					print(COLOR["RED"])
					print("  --Don't You Feel That's too much for a day ??--  ".rjust(50," "))
					print(COLOR["ENDC"])
			except ValueError:
				print(COLOR["RED"])
				print("--Enter An Integer Value--".rjust(40," "))
				print(COLOR["ENDC"])
		print(COLOR["Bold"])
		print("Enter Tasks one by one >>")
		for i in range(num):
			task=input()
			pd.add_task_in_db(task)
		in_date = str(self.in_date)
		in_time = str(self.in_time)
		pd.add_record(in_date,in_time)
		# pd.empty_pending_task_table()
		clear()
		print(COLOR["GREEN"],"NOW YOU ARE VIRTUALLY IN !!".rjust(54," "),COLOR["ENDC"])
		self.show_current_session()

	# SHOW CURRENT SESSION 
	def show_current_session(self):
		print(COLOR["BLUE"])
		print("""                     _______________________________________ """)
		print("""                    |                                       |""")
		print("""                    |             CURRENT SESSION           |""")
		print("""                    |_______________________________________|""")
		print(COLOR["ENDC"])
		pd.current_time_details()
		pd.show_tasks()
		self.ask_next_step()


	# # Ask whether completed a task or want to get virtually out 
	def ask_next_step(self):
		print()
		print(COLOR["GREEN"])
		print(" "*13,"1. COMPLETED A TASK ?  2.ADD A TASK  3. REMOVE A TASK ",COLOR["RED"])
		print()
		print("      ","4. <- GO BACK "," "*38,"5. LOG OUT ->")
		print(COLOR["ENDC"])
		choice = input('>>>    Enter your choice(Number) -> ')
		print(COLOR["Bold"])
		if choice == '1':
			# pd.show_tasks()
			print()
			position = input('>>>   Enter TaskId of task Completed -->  ')
			while type(position) is not int:
				try:
					position = int(position)
				except ValueError:
					print(COLOR["RED"])
					print("--Enter An Integer Value--".rjust(40," "))
					print(COLOR["ENDC"])
					position = input('>>>   Enter TaskId of task Completed -->  ')
					position = int(position)
			pd.Completed_a_task(position)
			clear()
			self.show_current_session()
		elif choice =='2':
			task = input(">>>    Enter Task You Want To ADD -> ")
			pd.add_task_in_db(task)
			clear()
			self.show_current_session()
		elif choice == '3':
			self.remove_task()
			clear()
			self.show_current_session()
		elif choice == '5':
			self.extra_tasks_accomplished()
		elif choice=='4':
			main_screen()
		else:
			print(COLOR["RED"],"                  ----ENTER INPUT FROM THE CHOICES GIVEN----    ",COLOR["ENDC"])
			self.ask_next_step()

	# # remove task
	def remove_task(self):
		print()
		position = input('>>>   Enter TaskId of task you want to remove -->  ')
		while type(position) is not int:
			try:
				position = int(position)
			except ValueError:
				print(COLOR["RED"])
				print("--Enter An Integer Value--".rjust(40," "))
				print(COLOR["ENDC"])
				position = input('>>>   Enter TaskId of task you want to remove -->  ')
				position = int(position)
		pd.remove_task_from_db(position)


	# # check if done extra tasks
	def extra_tasks_accomplished(self):
		ask = input(">>>>    Have you done any extra task also ? Y OR N -->  ")
		if ask=="Y" or ask =="y":
			print()
			n=input(">>>>    Enter Number of Extra Tasks Accomplished -->  ")
			while type(n) is not int:
				try:
					n=int(n)
				except ValueError:
					print()
					print(COLOR[RED],"--Enter An Integer Value--".rjust(40," "))
					print()
					n=input(">>>>    Enter Number of Extra Tasks Accomplished -->  ")
			print()
			print(">>>    Enter Your Tasks One By One")
			for i in range(n):
				k=input()
				self.extra_tasks_list.append(k)
			clear()
			self.virtually_out()
		elif ask=="N" or ask=="n":
			clear()
			self.virtually_out()
		else:
			print(COLOR["RED"],"      ----Invalid Choice !!---- ",COLOR["ENDC"])
			self.extra_tasks_accomplished()

	# # Making Status of user - OUT 
	def virtually_out(self):
		self.out_date = date.today()
		now = datetime.now()
		self.out_time = time(now.hour, now.minute, now.second)
		out_date = str(self.out_date)
		out_time = str(self.out_time)
		print(COLOR["RED"],"NOW YOU ARE VIRTUALLY OUT !!".rjust(55," "),COLOR["ENDC"])
		extra_task_len = len(self.extra_tasks_list)
		print(self.extra_tasks_list)
		pd.complete_record(out_date,out_time,extra_task_len)
		print()
		print("<<<<    EXTRA TASKS     >>>>")
		j=1
		for i in self.extra_tasks_list:
			print("  {}.  {}".format(j,i))
		print(COLOR["ENDC"])
		self.extra_tasks_list.clear()






		

person = schedule_management()

main_screen()


pd.close_database()