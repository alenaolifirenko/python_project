from random import randrange as rnd,choice
import tkinter as tk
import math
import time
root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root,bg='black')
canv.pack(fill = tk.BOTH,expand = 1)

dvdt = tk.DoubleVar()

scale = tk.Scale(root, variable = dvdt, orient = tk.HORIZONTAL)
scale.pack(side = tk.LEFT)


#Объект, которым мы управляем, ракета
class rocket():
	def __init__(self, x = 500, y = 500):
		self.x = x
		self.x0 = 0
		self.y0 = 0
		self.y = y
		self.r = 10
		self.vx = 0.5
		self.vy = 0
		self.fuel = 10 #запас топлива
		self.thrust = 1 #мощьность двигателя
		self.power = 0 #индикатор тяги
		self.ax = 0
		self.ay = 0
		self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill='red')
	def set_coords(self):
		canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)
	def positioning(self, event): #not used yet
		self.x0 = event.x
		self.y0 = event.y 
	def accel(self): #rocket acceleration
		global force, fd, power, screenx, screeny
		if power:
			x0 = screenx - self.x #acccel course
			y0 = screeny - self.y #acccel course
			self.ax = x0 / ((x0 ** 2 + y0 ** 2)) ** (1/2) / (self.fuel + 0.2) + force[0]
			self.ay = y0 / ((x0 ** 2 + y0 ** 2)) ** (1/2) / (self.fuel + 0.2) + force[1]
		else:
			self.ax = force[0]
			self.ay = force[1]

	def forced(self): #force commited on rocket
		global force, fd, n
		force = [0, 0]
		for i in range(n):
			fd[i].force(self.x, self.y)

	def move(self):
		global force, fd, dt
		self.forced()
		self.accel()
		self.x += (self.vx * dt + self.ax * dt ** 2 / 2) #Перемещение
		self.y += (self.vy * dt + self.ay * dt ** 2 / 2) #Перемещение
		self.vx += self.ax * dt
		self.vy += self.ay * dt
		if self.vx **2 + self.vy ** 2 > 1000:
			self.vx = self.vx * 0.8
			self.vy = self.vy * 0.8
		if self.x < 0 or self.x > 800:
			self.vx = - self.vx
		if self.y < 0 or self.y > 600:
			self.vy = - self.vy
		self.set_coords()
		print(dt)
		canv.update()
		root.after(50, self.move) #50мс - частота обновления
	def power_start(self, event):
		self.power = 1
	def power_end(self, event):
		self.power = 0
	
class field(): #недописано
	def __init__(self, x = 400 , y = 400, I = -1000):
		self.x = x
		self.y = y
		self.I = I
		self.r = 10
		self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill='blue')
	def force(self, x, y): #force in position x y
		global force
		force[0] += self.I * (x - self.x) / ((x - self.x) ** 2 + (y - self.y) ** 2) ** (3 / 2)
		force[1] += self.I * (y - self.y) / ((x - self.x) ** 2 + (y - self.y) ** 2) ** (3 / 2)
	def set_coords(self):
		canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

def positioning(event):
	global screenx, screeny
	screenx = event.x   #mouse position x
	screeny = event.y   #mouse position y

def power_start(event):
	global power
	power = 1 #power start trigger

def power_end(event):
	global power
	power = 0 #power end trigger

def time_speed_read():
	global dvdt, dt
	dt = dvdt.get() / 100
	root.after(100, time_speed_read)

def new_game(event = ''):
	global r1, force, fd, n, k, power, screenx, screeny, dt, dvdt
	force = [0, 0]
	power = 0
	time_speed_read() 
	n = 5 # number of fields
	k = 5 # number of rockets
	r = [rocket(rnd(100, 500)), rocket(rnd(100, 500)), rocket(rnd(100, 500)), rocket(rnd(100, 500)), rocket(rnd(100, 500))]
	fd = [field(rnd(100, 500), rnd(100, 500)), field(rnd(100, 500), rnd(100, 500)), field(rnd(100, 500), rnd(100, 500)), field(rnd(100, 500), rnd(100, 500)), field(rnd(100, 500), rnd(100, 500))]
	
	canv.bind('<Button-1>', power_start)
	canv.bind('<ButtonRelease-1>', power_end)
	canv.bind('<Motion>', positioning)


	for i in range(k):	
		r[i].move() #rocket launch
	#root.after(10,new_game)


new_game()

tk.mainloop()