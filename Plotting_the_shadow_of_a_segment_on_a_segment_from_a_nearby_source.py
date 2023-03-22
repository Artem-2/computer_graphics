from tkinter import *
import tkinter.messagebox as mb
from random import randint
from scipy.interpolate import *
import numpy as np
import math
import shapely
from shapely.geometry import LineString, Point

coords = 0
shadow_line_helper = []
line_point_helper_obstacle = []
shadow_line = []
point_helper_obstacle = 0
arr_point_helper_light = []
canvas_poligon = []
flag = None
mode = 0
number_line = 10
win = Tk()
win.title("Построение тени отрезка на отрезок от ближнего источника")
cv_wid = 950
cv_hgt = 600
r = 6
canvas = Canvas(win, width=590, height=590, borderwidth=1,highlightthickness=0)

def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False

def on_click_left_button(event):
    global arr_point_helper_light
    global number_point
    global flag
    global mode
    global point_helper_obstacle
    global line_point_helper_obstacle
    x, y = event.x, event.y
    r = 6
    if x>0 and y>0 and x<590 and y<590:
        if mode == 0:
            flag_helper = 0
            i = 0
            for a in arr_point_helper_light:
                if (x-a[0])**2 + (y-a[1])**2 - (r+2)**2 < 0:
                    flag_helper = 1
                    id = a[2]
                    j = i
                i = i + 1
            if flag_helper == 0:
                id_canvas = canvas.create_oval(x - r, y - r, x + r, y + r , outline="red",fill="red", width=0)
                canvas.place(x = 0, y = 0)
                arr_point_helper_light.append([x,y,id_canvas])
                mode = 1
            else:
                if flag == None:
                    flag = id,j,False,"light"
                else:
                    flag = None
        elif mode == 1:
            flag_helper = 0
            i = 0
            for a in line_point_helper_obstacle:
                if (x-a[0][0])**2 + (y-a[0][1])**2 - (r+2)**2 < 0:
                    flag_helper = 1
                    id = a[0][2]
                    j = i,0
                if (x-a[1][0])**2 + (y-a[1][1])**2 - (r+2)**2 < 0:
                    flag_helper = 1
                    id = a[1][2]
                    j = i,1
                i = i + 1
            if flag_helper == 0:
                for a in arr_point_helper_light:
                    if (x-a[0])**2 + (y-a[1])**2 - (r+2)**2 < 0:
                        flag_helper = 1
                        id = a[2]
                        j = i
                    i = i + 1
                if flag_helper == 0:
                    id_canvas = canvas.create_oval(x - r, y - r, x + r, y + r , fill='white', outline='black', width=2)
                    canvas.place(x = 0, y = 0)
                    point_helper_obstacle = [x,y,id_canvas]
                    mode = 2
                else:
                    if flag == None:
                        flag = id,j,False,"light"
                    else:
                        flag = None
            else:
                if flag == None:
                    flag = id,j,True,"obstacle"
                else:
                    flag = None
        elif mode == 2:
            flag_helper = 0
            a = point_helper_obstacle
            if (x-a[0])**2 + (y-a[1])**2 - (r+2)**2 < 0:
                flag_helper = 1
            if flag_helper == 0:
                id_canvas = canvas.create_oval(x - r, y - r, x + r, y + r , fill='white', outline='black', width=2)
                line_point_helper_obstacle.append((point_helper_obstacle,[x,y,id_canvas]))
                canvas.place(x = 0, y = 0)
                mode = 1
    create_ligth_line()
    
def distance(a,b,c):
    f = 0.1 #погрешность
    if c[0] - f < b[0] < c[0] + f and c[1] - f < b[1] < c[1] + f:
        return True 
    if a[0] - f < b[0] < a[0] + f and a[1] - f < b[1] < a[1] + f:
        return True 
    if a[0] <= b[0] <= c[0] or a[1]<= b[1] <= c[1]:
        return ((b[0] - a[0]) * (c[1] - a[1]) <= (c[0] - a[0]) * (b[1] - a[1]+f)) and ((b[0] - a[0]) * (c[1] - a[1]) >= (c[0] - a[0]) * (b[1] - a[1]-f)) or ((b[0] - a[0]) * (c[1] - a[1]) < (c[0] - a[0]) * (b[1] - a[1]-f)) and ((b[0] - a[0]) * (c[1] - a[1]) >= (c[0] - a[0]) * (b[1] - a[1]+f))
    return False

def create_ligth_line():
    global arr_point_helper_light
    global canvas_poligon
    if canvas_poligon != None:
        for c in canvas_poligon:
            canvas.delete(c)
        canvas_poligon.clear()
    shadow_line.clear()
    r = 6
    if len(arr_point_helper_light) > 0:
        for a_l in arr_point_helper_light:
            for a in line_point_helper_obstacle:
                a_helper_1 = a[1][0] + ((a_l[0] - a[1][0])*(-10))
                a_helper_2 = a[1][1] + ((a_l[1] - a[1][1])*(-10))
                point_1 = a_helper_1,a_helper_2
                a_helper_1 = a[0][0] + ((a_l[0] - a[0][0])*(-10))
                a_helper_2 = a[0][1] + ((a_l[1] - a[0][1])*(-10))
                point_2 = a_helper_1,a_helper_2
                number_intersection = 0
                if len(line_point_helper_obstacle) > 0:
                    i = 0 
                    for a1 in line_point_helper_obstacle:
                        line1 = LineString([(a_l[0],a_l[1]),point_1])
                        line2 = LineString([(a1[0][0],a1[0][1]),(a1[1][0],a1[1][1])])
                        int_pt = line1.intersection(line2)
                        if int_pt:
                            number_intersection = number_intersection + 1
                            shadow_line.append((int_pt.x, int_pt.y, i))
                        i = i + 1
                number_intersection = 0
                if len(line_point_helper_obstacle) > 0:
                    i = 0 
                    for a1 in line_point_helper_obstacle:
                        line1 = LineString([(a_l[0],a_l[1]),point_2])
                        line2 = LineString([(a1[0][0],a1[0][1]),(a1[1][0],a1[1][1])])
                        int_pt = line1.intersection(line2)
                        if int_pt:
                            number_intersection = number_intersection + 1
                            shadow_line.append((int_pt.x, int_pt.y, i))
                        i = i + 1
    if len(line_point_helper_obstacle) > 0:
        for a in line_point_helper_obstacle:
            canvas_poligon.append(canvas.create_line((a[0][0],a[0][1]),(a[1][0],a[1][1]),fill='green', width=2))
    #определение тени
    if len(shadow_line) > 0:
        shadow_itog = []
        i = 0 
        for a in line_point_helper_obstacle:
            shadow = []
            for a1 in line_point_helper_obstacle:
                if a != a1:
                    line1 = LineString([(a[0][0],a[0][1]),(a[1][0],a[1][1])])
                    line2 = LineString([(a1[0][0],a1[0][1]),(a1[1][0],a1[1][1])])
                    int_pt = line1.intersection(line2)
                    if int_pt:
                        flag_sl = 0
                        for s in shadow_line:
                            if s == (int_pt.x, int_pt.y):
                                flag_sl = 1
                        if flag_sl == 0:
                            shadow.append((int_pt.x, int_pt.y))
            for s in shadow_line:
                if s[2] == i:
                    shadow.append((s[0], s[1]))
            shadow_itog.append(shadow)
            i = i + 1
        j = 0
        for s in shadow_itog:
            if s != []:
                s2 = sorted(s)
                i = 0
                point_helper_flag = 0
                for s3 in range(len(s2)):
                    if i != len(s2)-1 and s2[i] != s2[i+1]:
                        point_1 = s2[i]
                        point_2 = s2[i+1]
                        point_3 = ((point_1[0] + point_2[0])/2,(point_1[1] + point_2[1])/2)
                        shadow_123 = []
                        ij = 0
                        for a in line_point_helper_obstacle:
                            if ij != j:
                                b = arr_point_helper_light[0]
                                line1 = LineString([(a[0][0],a[0][1]),(a[1][0],a[1][1])])
                                line2 = LineString([(b[0],b[1]),point_3])
                                int_pt = line1.intersection(line2)
                                if int_pt:
                                    shadow_123.append(point_3)
                            ij = ij + 1
                        if len(shadow_123) > 0:
                            if point_helper_flag == 0:
                                canvas_poligon.append(canvas.create_line((arr_point_helper_light[0][0],arr_point_helper_light[0][1]),s2[i],fill='red', width=2))
                                point_helper_flag = 1
                            canvas_poligon.append(canvas.create_line(point_1,point_2,fill='black', width=10))
                        else:
                            if point_helper_flag == 1:
                                canvas_poligon.append(canvas.create_line((arr_point_helper_light[0][0],arr_point_helper_light[0][1]),s2[i],fill='red', width=2))
                                point_helper_flag = 0
                    i = i + 1
                if point_helper_flag == 1:
                    canvas_poligon.append(canvas.create_line((arr_point_helper_light[0][0],arr_point_helper_light[0][1]),s2[i-1],fill='red', width=2))
            j = j + 1

def mouse(event):
    global arr_point_helper_light
    global canvas_poligon
    global flag
    global mode
    if event.x < 590 and event.x > 10 and event.y < 590 and event.y > 10:
        if flag != None and (len(arr_point_helper_light) > 0 or len(line_point_helper_obstacle) > 0):
            if mode == 0 or (mode == 1 and flag[3] == "light"):
                coords.config(text="координаты выбраной точки: " + str(int(event.x)) + ":" + str(int(event.y)))
                if canvas_poligon != None:
                    x, y = event.x, event.y
                    arr_point_helper_light[0][0] = x
                    arr_point_helper_light[0][1] = y
                    for c in canvas_poligon:
                        canvas.delete(c)
                    canvas_poligon.clear()
                    canvas.coords(flag[0],x - r, y - r, x + r, y + r)
                    create_ligth_line()
                else:
                    x, y = event.x, event.y
                    arr_point_helper_light[flag[1]][0] = x
                    arr_point_helper_light[flag[1]][1] = y
                    canvas.coords(flag[0],x - r, y - r, x + r, y + r)
            elif mode == 1 and flag[3] != "light":
                coords.config(text="координаты выбраной точки: " + str(int(event.x)) + ":" + str(int(event.y)))
                if canvas_poligon != None:
                    x, y = event.x, event.y
                    line_point_helper_obstacle[flag[1][0]][flag[1][1]][0] = x
                    line_point_helper_obstacle[flag[1][0]][flag[1][1]][1] = y
                    for c in canvas_poligon:
                        canvas.delete(c)
                    canvas_poligon.clear()
                    canvas.coords(flag[0],x - r, y - r, x + r, y + r)
                    create_ligth_line()
                else:
                    x, y = event.x, event.y
                    line_point_helper_obstacle[flag[1][0]][flag[1][1]][0] = x
                    line_point_helper_obstacle[flag[1][0]][flag[1][1]][1] = y
                    canvas.coords(flag[0],x - r, y - r, x + r, y + r)
        if flag == None:
                coords.config(text="координаты выбраной точки: " + str(int(event.x)) + ":" + str(int(event.y)))
def delete_all():
    global arr_point_helper_light
    global canvas_poligon
    global number_point
    global mode
    if len(arr_point_helper_light) != 0:
        for a in arr_point_helper_light:
            canvas.delete(a[2])
            number_point = 1
        arr_point_helper_light.clear()
    if len(line_point_helper_obstacle) != 0:
        for a in line_point_helper_obstacle:
            canvas.delete(a[0][2])
            canvas.delete(a[1][2])
            number_point = 1
        line_point_helper_obstacle.clear()
    if canvas_poligon != None:
        for c in canvas_poligon:
            canvas.delete(c)
        canvas_poligon.clear()
    mode = 0

if __name__ == "__main__":
    win.geometry(str(cv_wid)+"x" + str(cv_hgt))
    window = 1,1,1,590,590,590,590,1
    canvas.create_polygon(window, outline='grey', fill = "white", width=2)
    canvas.bind('<Button-1>', on_click_left_button)
    canvas.bind('<Motion>', mouse)
    canvas.place(x = 0, y = 0)
    btn = Button(win, text="очистить", command=delete_all)
    btn.place(x = 620, y = 130)
    label1 = Label(text="Первым нажатием создается ближний источник света", fg="#333", bg="#eee")
    label1.place(x = 620, y = 230)
    label1 = Label(text="последующие нажатия создают препятствия", fg="#333", bg="#eee")
    label1.place(x = 620, y = 245)
    label1 = Label(text="Для создания источника света, препятствия необходимо нажать ЛКМ", fg="#333", bg="#eee")
    label1.place(x = 620, y = 260)
    label1 = Label(text="Для передвижения необходимо нажать ЛКМ", fg="#333", bg="#eee")
    label1.place(x = 620, y = 275)
    label1 = Label(text="на точку которую необходимо переместить ", fg="#333", bg="#eee")
    label1.place(x = 620, y = 290)
    coords = Label(text="координаты выбраной точки: 0:0", fg="#333", bg="#eee")
    coords.place(x = 620, y = 440)
    win.protocol("WM_DELETE_WINDOW", win.quit)
    win.mainloop()