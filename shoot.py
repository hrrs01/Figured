import sys
import math
import copy
import time
import os
import re

class Shoot:
	
	def __init__(self):
		
		self.basic_commands = {"<": self.left, ">": self.right, "^": self.shoot, ".": self.idle}
	
		self.grid = []
		self.grid_show = []
		self.reflectors = {"H": self.special_reflector_down, "Z": self.special_reflector_right, "/": self.reflector_nw, "\\": self.reflector_ne, "V": self.reflector_down}
		self.targets = {"%": self.modulo,">": self.left, "<": self.right, "^": self.shoot,"+": self.add, "-": self.sub, ":": self.divide, "*": self.multiply, "O": self.output, "I": self.input, "A": self.new_variable, "Ø": self.flush}
		
		self.basic = ""
		
		self.bullet_index = 0
		
		self.bullets = [] 
		
		self.shooter_index = 0
		self.variables = []
		
		
		
		self.divider = "|"
		
		self.outputstream = ""
		
		self.file = None
		
	# Targets
	
	def add(self, x):
		x["v"] += self.variables[self.shooter_index]
	
	def sub(self, x):
		x["v"] -= self.variables[self.shooter_index]
		
	def divide(self, x):
		x["v"] /= self.variables[self.shooter_index]
		
	def multiply(self, x):
		x["v"] *= self.variables[self.shooter_index]
		
	def output(self, x):
		self.outputstream += chr(x["v"])
	
	def flush(self,x):
		self.outputsteam = ""
	
	def modulo(self,x):
		x["v"] %= self.variables[self.shooter_index]
	
	def input(self, x):
		x["v"] = ord(input()[0])
	
	def new_variable(self, x):
		self.variables.append(x["v"])
		for i,x in enumerate(self.grid):
			x.append(self.grid[i][self.shooter_index])
	
	# Basic Commands / targets
	def left(self, x):
		if self.shooter_index > 0:
			self.shooter_index -= 1
	
	def right(self, x):
		if self.shooter_index < len(self.variables)-1:
			self.shooter_index += 1
	
	def idle(self):
		pass
		
	# Reflectors
	def reflector_right(self, x):
		x["d"] = "e"
	
	
	def reflector_down(self, x):
		x["d"] = "s"
	
	def reflector_up(self, x):
		x["d"] = "n"

	def reflector_left(self, x):
		x["d"] = "w"
	
	def special_reflector_down(self, x):
		if x["v"] == self.variables[self.shooter_index]:
			x["d"] = "n"
		else:
			x["d"] = "s"
	
	def special_reflector_right(self, x):
		if x["v"] == self.variables[self.shooter_index]:
			x["d"] = "w"
		else:
			x["d"] = "e"
		
	def reflector_ne(self, x):
		if x["d"] == "s":
			x["d"] = "e"
		elif x["d"] == "n":
			x["d"] = "w"
		elif x["d"] == "e":
			x["d"] = "s"
		elif x["d"] == "w":
			x["d"] = "n"
	
	def reflector_nw(self, x):
		if x["d"] == "s":
			x["d"] = "w"
		elif x["d"] == "n":
			x["d"] = "e"
		elif x["d"] == "e":
			x["d"] = "n"
		elif x["d"] == "w":
			x["d"] = "s"
		
	#Loading logic
	def open_file(self):
		self.file = open(sys.argv[1], "r")
		temp = self.file.read()
		temp = re.sub(r'\#.*\#', "", temp)
		temp2 = temp.split("_")
		self.update_variables(temp2[1])
		self.update_grid(temp2[0])
		self.basic = temp2[2]
	
	
	def update_grid(self, g):
		for x in g.split("|"):
			x = [y for y in x]
			self.grid.append(x)
		
		for x in self.grid:
			while len(x) < len(self.variables):
				x.append(".")
			
			while len(x) > len(self.variables):
				x.pop()
	
	def update_variables(self, v):
		self.variables = [x for x in v.split("|") if x is not ""]
		for i,x in enumerate(self.variables):
			if x.isalpha():
				self.variables[i] = ord(x)
			else:
				self.variables[i] = int(x)
				
	
	
	# Gunner
	
	def shoot(self, x):
		self.bullets.append({"d": "n", "x": self.shooter_index, "y": len(self.grid), "v": int(self.variables[self.shooter_index])})
	
	
	
	
		
			
	# Calculations
	
	def calc(self):
		self.grid_show = copy.deepcopy(self.grid)
		for z in self.bullets:
				
				
				
				if z["d"] == "n":
					if z["y"] > 0: 
						z["y"] -= 1
					else:
						self.bullets.remove(z)
						continue
				elif z["d"] == "s":
					if z["y"] < len(self.grid)-1:
						z["y"] += 1
					else:
						self.variables[z["x"]] = z["v"]
						self.bullets.remove(z)
						
						continue
				elif z["d"] == "e":
					if z["x"] < len(self.variables)-1:
						z["x"] += 1
					else:
						self.bullets.remove(z)
						continue
				elif z["d"] == "w":
					if z["x"] > 0:
						z["x"] -= 1
					else:
						self.bullets.remove(z)
						continue
			
				if self.grid[z["y"]][z["x"]] in self.reflectors:
					self.reflectors[self.grid[z["y"]][z["x"]]](z)
				
				if self.grid[z["y"]][z["x"]] in self.targets:
					self.targets[self.grid[z["y"]][z["x"]]](z)
				
				#print(z["y"])
				#print(z["x"])
				self.grid_show[z["y"]][z["x"]] = z["v"]
			
			
			#print(self.grid)
			
			#print(x)
			

		time.sleep(float(sys.argv[2]) if len(sys.argv)>2 else 1)
		os.system("cls")
		print(self.grid_show)
		if self.outputstream != "":
			print(self.outputstream)
	
		print(self.variables)
		
	def run(self):
		self.open_file()
		
		for x in self.basic:
			
			self.basic_commands[x](x)
			
			self.calc()
			
			
		while self.bullets:
			self.calc()
			
		
		
if __name__ == "__main__":
	f = Shoot()
	f.run()