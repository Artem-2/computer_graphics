from tkinter import *
from scipy.linalg import solve
import numpy as np
import math
import tkinter.messagebox as mb


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
    win.mainloop()