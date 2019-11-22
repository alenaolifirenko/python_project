from random import randrange as rnd, choice
import tkinter as tk
import math

import time

# Объект, которым мы управляем, ракета
class rocket():
    def __init__(self, x=500, y=500, vx=0, vy=0, canvas=None):

        self.canv = canvas
        self.x = x
        self.x0 = 0
        self.y0 = 0
        self.y = y
        self.r = 10
        self.vx = vx
        self.vy = vy
        self.fuel = 0.8  # fuel capacity
        self.thrust = 0.03  # thurst power
        self.power = 0  # power indicator
        self.ax = 0  # acceleration
        self.ay = 0  # acceleration
        self.id = self.canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill='red')
        self.dax = 0  # former acceleration
        self.day = 0  # former acceleration

    def set_coords(self):
        self.canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    '''def positioning(self, event):
        self.x0 = event.x
        self.y0 = event.y'''

    def accel(self):  # rocket acceleration
        global force, power, screenx, screeny, dt
        self.dax = self.ax  # remembering former acceleraion
        self.day = self.ay

        if power:
            x0 = screenx - self.x  # acccel course
            y0 = screeny - self.y  # acccel course
            if self.fuel > 0:
                self.fuel -= 0.01 * dt
                self.ax = self.thrust * dt * x0 / ((x0 ** 2 + y0 ** 2)) ** (1 / 2) / (self.fuel + 0.2) + force[
                    0]  # new acceleration if power on
                self.ay = self.thrust * dt * y0 / ((x0 ** 2 + y0 ** 2)) ** (1 / 2) / (self.fuel + 0.2) + force[1]
            else:
                self.ax = force[0]  # new acceleration if power on and no fuel
                self.ay = force[1]
        else:
            self.ax = force[0]  # new acceleration if power off
            self.ay = force[1]
        #displayed_fuel.set(str(self.fuel)[0:4] + " топлива осталось")  # fuel indicator

    def forced(self):  # force commited on rocket
        global force, pl, n, m, mn
        force = [0, 0]
        for i in range(n):
            pl[i].force(self.x, self.y)
        for i in range(m):
            mn[i].force(self.x, self.y)

    def move(self):
        global dt
        self.forced()
        self.accel()
        self.x += (self.vx * dt + self.ax * dt ** 2 / 2 + (self.ax - self.dax) * dt ** 2 / 3)  # Перемещение
        self.y += (self.vy * dt + self.ay * dt ** 2 / 2 + (self.ay - self.day) * dt ** 2 / 3)  # Перемещение
        # self.x += (self.vx * dt) #Перемещение
        # self.y += (self.vy * dt) #Перемещение

        self.vx += self.ax * dt
        self.vy += self.ay * dt
        if self.vx ** 2 + self.vy ** 2 > 1000:
            self.vx = self.vx * 0.8
            self.vy = self.vy * 0.8
        if self.x < 0 or self.x > 800:
            self.vx = - self.vx
        if self.y < 0 or self.y > 600:
            self.vy = - self.vy
        self.set_coords()
        self.canv.update()
        root.after(5, self.move)  # 10мс - частота обновления

    def power_start(self, event):
        self.power = 1

    def power_end(self, event):
        self.power = 0


class planet():
    def __init__(self, x=400, y=400, I=-1000, canvas=None):
        self.canv = canvas
        self.x = x
        self.y = y
        self.I = I
        self.r = 10
        self.id = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill='blue')

    def force(self, x, y):  # force in position x y
        global force
        force[0] += self.I * (x - self.x) / ((x - self.x) ** 2 + (y - self.y) ** 2) ** (3 / 2)
        force[1] += self.I * (y - self.y) / ((x - self.x) ** 2 + (y - self.y) ** 2) ** (3 / 2)

    def set_coords(self):
        canvas.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)


class moon():
    def __init__(self, planet, R, r, I=-50, cw=1, phase=0, colour='green', canvas=None):
        self.canv = canvas
        self.pl = planet
        self.R = R
        self.r = r
        self.I = I
        if cw:
            self.W = 10 * planet.I / self.R ** 3
        else:
            self.W = - 10 * planet.I / self.R ** 3
        self.phase = phase
        self.x = 0
        self.y = 0
        self.colour = colour
        self.id = self.canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.colour)

    def force(self, x, y):  # force in position x y
        global force
        force[0] += self.I * (x - self.x) / ((x - self.x) ** 2 + (y - self.y) ** 2) ** (3 / 2)
        force[1] += self.I * (y - self.y) / ((x - self.x) ** 2 + (y - self.y) ** 2) ** (3 / 2)

    def set_coords(self):
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)

    def move(self):
        global dt

        self.phase += self.W * dt
        self.x = self.pl.x + self.R * math.cos(self.phase)
        self.y = self.pl.y + self.R * math.sin(self.phase)

        # print(self.phase)
        self.set_coords()
        canv.update()
        root.after(5, self.move)