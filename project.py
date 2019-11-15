from random import randrange as rnd,choice
from tkinter import*
import math
import time
root=Tk()
fr=Frame(root)
root.geometry('800x600')
canv=Canvas(root,bg='white')
canv.pack(fill=BOTH,expand=1)

#Объект, которым мы управляем, ракета
class rocket():
	def __init__(self, x = 500, y = 500):
		self.x = x
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
	def forced(self, event): #ускорение ракеты
		global force
		if self.power:
			x0 = event.x - self.x #наведение ускорения
			y0 = event.y - self.y #наведение ускорения
			self.ax = x0 / ((x0 ** 2 + y0 ** 2)) ** (1/2) / (self.fuel + 0.2) + force[0]
			self.ay = y0 / ((x0 ** 2 + y0 ** 2)) ** (1/2) / (self.fuel + 0.2) + force[1]
		else:
			self.ax = force[0]
			self.ay = force[1]
	def move(self):
		self.x += (self.vx + self.ax / 2) #Перемещение
		self.y += (self.vy + self.ay / 2) #Перемещение
		self.vx += self.ax
		self.vy += self.ay
		if self.x < 0 or self.x > 800:
			self.vx = - self.vx
		if self.y < 0 or self.y > 600:
			self.vy = - self.vy
		self.set_coords()
		canv.update()
		root.after(50, self.move) #50мс - частота обновления
	def power_start(self, event):
		self.power = 1
	def power_end(self, event):
		self.power = 0
	
class field(): #недописано
	def __init__(self, x = 0, y = 0, I = 1):
		self.x = x
		self.y = y
		self.I = I
		self.r = 10
		self.id = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill='red')
	def force(self, x, y):
		global force
		force[0] = I * x / (x ** 2 + y ** 2) ** (3 / 2)
		force[1] = I * y / (x ** 2 + y ** 2) ** (3 / 2)
		return force

def new_game(event = ''):
	global r1, force
	force = [0, 0] 
	r1 = rocket()
	canv.bind('<Button-1>', r1.power_start) #тяга при нажатии
	r1.move()
	canv.bind('<ButtonRelease-1>', r1.power_end) #нет тяги при отпускании
	canv.bind('<Motion>', r1.forced) #наведение мышкой
	#root.after(10,new_game)


new_game()

mainloop()