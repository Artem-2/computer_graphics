from tkinter import *
from scipy.linalg import solve
import numpy as np
import math
import tkinter.messagebox as mb


class point:
    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z
    def minus(point_1, point_2):
        A = point(0, 0, 0)
        A.X = point_1.X - point_2.X
        A.Y = point_1.Y - point_2.Y
        A.Z = point_1.Z - point_2.Z
        return A
    def multiplication(point_1, point_2):
        A = point(0, 0, 0)
        A.X = (point_1.Y * point_2.Z) - (point_1.Z * point_2.Y)
        A.Y = (point_1.Z * point_2.X) - (point_1.X * point_2.Z)
        A.Z = (point_1.X * point_2.Y) - (point_1.Y * point_2.X)
        return A


class edge:
    def __init__(self, points):
        self.points = points
        self.normal = point.multiplication(point.minus(points[1], points[0]),point.minus(points[2], points[0]))

vector_camera = point(-1,0,0)

A = edge([point(0,0,0), point(0,1,0), point(0,1,1), point(0,0,1)])
print(A.normal.X, A.normal.Y, A.normal.Z)

win = Tk()
win.title("Исследование существования и построение циклических и ациклических интерполяционных линий")
cv_wid = 950
cv_hgt = 600
r = 6
number_point = 1
canvas = Canvas(win, width=cv_wid, height=cv_hgt, borderwidth=1,highlightthickness=0)



if __name__ == "__main__":
    win.geometry(str(cv_wid)+"x" + str(cv_hgt))
    window = 10,10,10,590,590,590,590,10
    canvas.place(x = 0, y = 0)
    canvas.create_polygon(window, outline='grey', fill = "white", width=2)
    opred1 = Label(text="", fg="#333", bg="#eee")
    opred1.place(x = 620, y = 330)
    win.protocol("WM_DELETE_WINDOW", win.quit)
    #win.mainloop()