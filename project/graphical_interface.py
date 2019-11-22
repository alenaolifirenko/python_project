import tkinter as tk
import classes as c
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='black')
canv.pack(fill=tk.BOTH, expand=1)

dvdt = tk.DoubleVar()

scale = tk.Scale(root, variable=dvdt, orient=tk.HORIZONTAL)
scale.pack(side=tk.LEFT)

displayed_fuel = tk.StringVar()

fuel_label = tk.Label(root, textvariable=displayed_fuel, width=30)
fuel_label.pack(side=tk.RIGHT)

def positioning(event):
    global screenx, screeny
    screenx = event.x  # mouse position x
    screeny = event.y  # mouse position y


def power_start(event):
    global power
    power = 1  # power start trigger


def power_end(event):
    global power
    power = 0  # power end trigger


def time_speed_read():
    global dvdt, dt
    dt = dvdt.get() / 100
    root.after(100, time_speed_read)


def new_game(event=''):
    global r, force, pl, n, k, power, screenx, screeny, dt, dvdt, m, mn
    force = [0, 0]
    power = 0
    time_speed_read()
    n = 1  # number of fields
    k = 1  # number of rockets
    m = 1  # number of moons
    r = [c.rocket(300, 350, 4.47, 0, canv)]
    pl = [c.planet(300, 300, canvas=canv)]
    mn = [c.moon(pl[0], 100, 5, -30, 0, -1.62, canvas=canv)]

    displayed_fuel.set(str(r[0].fuel) + " seconds gone")
    canv.bind('<Button-1>', power_start)
    canv.bind('<ButtonRelease-1>', power_end)
    canv.bind('<Motion>', positioning)

    for i in range(k):
        r[i].move()  # rocket launch
    # root.after(10,new_game)
    for i in range(m):
        mn[i].move()
