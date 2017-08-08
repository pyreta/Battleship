#Player Class ************************

class Player(object):
	def __init__(self,player_type="human"):
		self.rows = ['A','B','C','D','E','F','G','H','I','J']
		self.columns = []
		for i in range(1,11):
			self.columns.append(str(i))

		self.aircraft_carrier = {"symbol":"AAAAA", "length": 5, "start":["A","6"], "direction":"vertical", "name":"Aircraft Carrier", "status":"inactive", "hits":0, "coordinates":[]}
		self.battleship = {"symbol":"BBBB", "length": 4, "start":["G","4"], "direction":"vertical", "name":"Battleship", "status":"inactive", "hits":0, "coordinates":[]}
		self.submarine = {"symbol":"SSS", "length": 3, "start":["C","7"], "direction":"vertical", "name":"Submarine", "status":"inactive", "hits":0, "coordinates":[]}
		self.cruiser = {"symbol":"CCC", "length": 3, "start":["G","5"], "direction":"horizontal", "name":"Cruiser", "status":"inactive", "hits":0, "coordinates":[]}
		self.destroyer = {"symbol":"DD", "length": 2, "start":["A","1"], "direction":"horizontal", "name":"Destroyer", "status":"inactive", "hits":0, "coordinates":[]}

		self.battleships = [self.aircraft_carrier,self.battleship,self.submarine,self.cruiser,self.destroyer]
		self.all_axis = []
		self.hits = []
		self.misses = []
		self.sunken_ships = 0

		self.player_type = player_type

		self.place_ships()
		for i in range(50):
			print ""

#Class Functions ************************

	def place_ships(self):
		if self.player_type == "human":
			print "***** Welcome to Battleship.  Don't Cheat.*****"
			print "Type quit at any time."  
			print ""
		for ship in self.battleships:
			if self.player_type == "computer":
				self.place_ship_computer(ship)
			else:
				self.place_ship_human(ship)	

	def place_ship_human(self,ship):

		self.printgrid()
		print ""
		start = raw_input(
							"Place your "
							+ship["name"]
							+" ("
							+str(len(ship["symbol"]))
							+" spaces)"
							+": "
							)
		if start == "quit":
			raise SystemExit 		
		formatted_start = start[0].upper()+start[-1]
		# while formatted_start in self.all_axis:
		# 	start = raw_input("Nope, try again.. ")
		print ship["name"],"placed on",start	
		direction = str(raw_input("horizontal or vertical? (h,v): ")).lower()
		if direction == "quit":
			raise SystemExit 
		while "v" not in direction and "h" not in direction:
			direction = str(raw_input("Again... horizontal or vertical? ")).lower()	
		print ""

		if len(start) == 2:
			ship["start"] = [start[0].upper(),start[1]]
		else:
			ship["start"] = [start[0].upper(),start[1]+start[2]]

		if "v" in direction:
			direction = "vertical"
		else:
			direction = "horizontal"		

		print "ship start",ship["start"]
		ship["direction"]=direction
		ship["status"] = "active"
		self.set_ship_coordinates(ship)

		test_pass = True
		for i in ship["coordinates"]:
			if i in self.all_axis or int(i[1:]) > 10:
				test_pass = False


		if test_pass == True:
			self.all_axis.extend(ship["coordinates"])
			self.printgrid()
		else:
			ship["status"] = "inactive"
			print "Sorry, can't put your ship there.  Try again."
			self.place_ship_human(ship)	
		for i in range(50):
			print ""	

	def set_ship_coordinates(self,ship):
		row = ship["start"][0].upper()
		column = int(ship["start"][1])
		axis = []
		if ship["direction"] == "horizontal":
					
			for i in range(ship["length"]):
				point = row + str(i+column)
				axis.append(point)
		else:
			while self.rows.index(row) + ship["length"] > 10:
				row = self.rows[randrange(0,10)]
				print "row re-do",row	
			for i in range(ship["length"]):
				row_index = self.rows.index(row)
				point = self.rows[row_index+i] + str(column)
				axis.append(point)
		ship["coordinates"] = axis 		

	def place_ship_computer(self,ship):
		directions = ["horizontal","vertical"]
		# print ""
		# print "*********",ship["name"]
		# print "length:", ship["length"]
		ship["direction"] = directions[randrange(0,2)]
		# print ship["direction"]

		row = self.rows[randrange(0,10)]
		# print "row",row

		column = randrange(1,11)
		# print "column", column

		axis = []
		if ship["direction"] == "horizontal":
			while column + ship["length"] > 10:
				column = randrange(1,11)
				# print "column re-do", column						
			for i in range(ship["length"]):
				point = row + str(i+column)
				axis.append(point)
		else:
			while self.rows.index(row) + ship["length"] > 10:
				row = self.rows[randrange(0,10)]
				# print "row re-do",row	
			for i in range(ship["length"]):
				row_index = self.rows.index(row)
				point = self.rows[row_index+i] + str(column)
				axis.append(point)
		# print axis 

		test_pass = True
		for i in axis:
			# print i
			# print self.all_axis
			if i in self.all_axis:
				test_pass = False
			# print test_pass	

		if test_pass == True:
			# print "PASSED"
			self.all_axis.extend(axis)
			ship["start"] = row+str(column)
			ship["coordinates"] = axis 
			ship["status"] = "active"
			# print "ALL AXISS",self.all_axis
		else:
			# print "UH OH DOING IT AGAIN!!!!"
			self.place_ship_computer(ship)					
			
	def show_ships_in_row(self,row):
		string_list = []
		ship_is_here = False
		for i in range(10):
			# coordinate = [row,str(i+1)]
			coordinate = row+str(i+1)
			for ship in self.battleships:

				if coordinate in ship["coordinates"] and ship["status"]!= "inactive":
					# print "YEAHHH ITS HERE!!"
					if coordinate not in self.hits:
						string_list.append(ship["symbol"][0] + " ")
					else:
						string_list.append(ship["symbol"][0].lower() + " ")	
					ship_is_here = True


			if ship_is_here == False:
				string_list.append("  ")
			else:	
				ship_is_here = False	
		return "".join(string_list)			

	def show_attacks_in_row(self,row):
		string_list = []
		ship_is_here = False
		for i in range(10):
			# coordinate = [row,str(i+1)]
			coordinate = row+str(i+1)


			if coordinate in self.hits:
				string_list.append("X ")
				ship_is_here = True
			elif coordinate in self.misses:
				string_list.append("o ")
				ship_is_here = True
					



			if ship_is_here == False:
				string_list.append("  ")
			else:	
				ship_is_here = False	
		return "".join(string_list)			

	def printgrid(self,show_shots_taken = False):
		self.battleships = sorted(self.battleships,key=lambda ship:int(ship["start"][1]))
		print ""	
		print " "," ".join(self.columns)
		print "  ____________________"
		for i in self.rows:
			if show_shots_taken == True:
				print i+"|"+self.show_attacks_in_row(i) 
			else:
				print i+"|"+self.show_ships_in_row(i) 	
		print ""		

	def printships(self):
		print "Aircraft Carrier -", self.aircraft_carrier["status"], ", Hits -",self.aircraft_carrier["hits"]
		print "Battleship -", self.battleship["status"], ", Hits -",self.battleship["hits"]
		print "Submarine -", self.submarine["status"], ", Hits -",self.submarine["hits"]
		print "Cruiser -", self.cruiser["status"], ", Hits -",self.cruiser["hits"]
		print "Destroyer -", self.destroyer["status"], ", Hits -",self.destroyer["hits"]

#Program Functions ************************

def shoot_graphic():
	for i in range(100):
		print ""
	tally = 0	
	for i in range(48):	
		bullet = " "*tally+"*"	

		print "                                                             ____ "
		print "___________                                              ____|__|____ "
		print "__________|"+bullet+(45-tally)*" "+"\__________"
		tally += 1
		time.sleep(.015)
		for i in range(100):
			print ""	

def take_shot_human(shooter,target):
	for i in range(50):
		print ""
	print "****** YOUR SHIPS (" +str(5 - shooter.sunken_ships) +" still floating) *******"
	shooter.printgrid()
	print ""
	# target.printgrid()
	# print ""	
	if target.sunken_ships == 4:
		shipword = "ship"
	else:
		shipword = "ships"	
	print "****** FIRING HISTORY (" +str(5 - target.sunken_ships) +" enemy "+shipword+" remaining) *******"
	target.printgrid(show_shots_taken = True)
	print ""	
	shot = raw_input("Take a shot: ")	
	if shot == "quit":
		raise SystemExit
	shot = shot[0].upper()+shot[1:]
	shoot_graphic()
	if shot in target.hits:
		if shooter.player_type == "human":
			print "You already fired here.."
	if shot in target.all_axis:
		mark_hit(shot,target)
	else:
		print "miss..."	
		target.misses.append(shot)
	time.sleep(1)
	for i in range(50):
		print ""
	print "Prepare to be blasted at!"
	time.sleep(1)			

def take_shot_computer(shooter,target):
	shot = computer_shot(target, shooter)	
	shoot_graphic()
	if shot in target.all_axis:
		for i in range(25):
			for x in range(100):
				print ""
			print "You've been HIT!"+(i*"!")
			time.sleep(.015)

		time.sleep(1)
		mark_hit(shot,target)	

	else:
		print "You just got missed.."
		time.sleep(1)				

def mark_hit(shot,target):

	target.all_axis.remove(shot)
	target.hits.append(shot)
	for ship in target.battleships:
		if shot in ship["coordinates"]:
			ship["hits"] += 1
			if target.player_type == "human":
				print "Your "+ship["name"]+" has been HIT at "+shot 
			else:	
				print "Enemy ship HIT at "+shot 
			time.sleep(1)			
			if ship["hits"] == len(ship["symbol"]) and ship["status"] != "sunken":
				ship["status"] = "sunken"
				target.sunken_ships += 1
				print ship["name"] + " has been sunken!"
				time.sleep(1)


			if target.sunken_ships == 5:
				print "GAME OVER!!!"
				time.sleep(1)
				if target.player_type == "computer":
					for i in range(50):
						for x in range(50):
							print ""
						print "You WIN!"+(i*"!")
						time.sleep(.015)

				else:
					print "You Lose."
					time.sleep(1)
					for i in range(50):
						print ""
					print "Goodbye."	
				raise SystemExit			
			return 

def computer_shot(shooter,target):
	"Computer shooting you..."
	row = shooter.rows[randrange(0,10)]
	column = str(randrange(1,11))
	coordinate = [row,column]
	print "Enemy firing..."
	time.sleep(1)
	return "".join(coordinate)

#Lets gO! *********************************

import time 
from random import randrange

for i in range(100):
	print ""

computer = Player(player_type="computer")
player = Player()

while True:
	take_shot_human(player, computer)
	take_shot_computer(computer, player)
