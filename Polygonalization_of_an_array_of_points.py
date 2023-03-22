from tkinter import *
import tkinter.messagebox as mb
from random import randint
import math

coords = 0
arr_point_helper = []
canvas_poligon = None
flag = None
win = Tk()
win.title("Полигонализация массива точек (poly_point)")
cv_wid = 950
cv_hgt = 600
r = 6
canvas = Canvas(win, width=cv_wid, height=cv_hgt, borderwidth=1,highlightthickness=0)


def on_click_left_button(event):
    global arr_point_helper
    x, y = event.x, event.y
    r = 6
    if x>10 and y>10 and x<590 and y<590:
        flag_helper = 0
        i = 0
        id = 0
        for a in arr_point_helper:
            if (x-a[0])**2 + (y-a[1])**2 - (r+2)**2 <= 0:
                flag_helper = 1
                id = a[2]
                j = i
            i = i + 1
        if flag_helper == 0:
            id_canvas = canvas.create_oval(x - r, y - r, x + r, y + r , outline="green",fill="green", width=0)
            canvas.place(x = 0, y = 0)
            arr_point_helper.append([x,y,id_canvas])
        else:
            global flag
            if flag == None:
                flag = id,j
            else:
                flag = None
    if canvas_poligon != None:
        canvas.delete(canvas_poligon)
        create_poligon()

def distance(a,b,c):
    f = 1 #погрешность
    return ((b[0] - a[0]) * (c[1] - a[1]) <= (c[0] - a[0]) * (b[1] - a[1]+f)) and ((b[0] - a[0]) * (c[1] - a[1]) >= (c[0] - a[0]) * (b[1] - a[1]-f)) or ((b[0] - a[0]) * (c[1] - a[1]) < (c[0] - a[0]) * (b[1] - a[1]-f)) and ((b[0] - a[0]) * (c[1] - a[1]) >= (c[0] - a[0]) * (b[1] - a[1]+f))

def create_poligon():
    global arr_point_helper
    global canvas_poligon
    if canvas_poligon != None:
        canvas.delete(canvas_poligon)
    if len(arr_point_helper) > 1:
        arr_point = []
        for a in arr_point_helper:
            arr_point.append([a[0],a[1]])
        leftmost_point, *_, rightmost_point = sorted(arr_point, key=lambda lst: lst[0])

        x1, y1 = leftmost_point
        x2, y2 = rightmost_point

        border_slope = (y2 - y1) / (x2 - x1)

        points_below_border = [(x1, y1)]
        points_above_border = [(x2, y2)]
        for x, y in arr_point:
            border = border_slope * (x - x1) + y1
            if y < border:
                points_below_border.append((x, y))
            elif y > border:
                points_above_border.append((x, y))

        points_below_border.sort()
        points_above_border.sort(reverse=True)
        arr_point = points_below_border + points_above_border
        
        arr_point_2 = []
        f = len(arr_point)
        for i in range(f):
            if i == 0:
                a = arr_point[f-1]
                b = arr_point[i]
                c = arr_point[i+1]
            elif i < f-1:
                a = arr_point[i-1]
                b = arr_point[i]
                c = arr_point[i+1]
            else:
                a = arr_point[i-1]
                b = arr_point[i]
                c = arr_point[0]
            if distance(a,b,c):
                f2 = len(arr_point_helper)
                for j in range(f2):
                    if arr_point_helper[j][0] == arr_point[i][0] and arr_point_helper[j][1] == arr_point[i][1]:
                        canvas.itemconfig(arr_point_helper[j][2], fill='black', outline='black')
            else:
                f2 = len(arr_point_helper)
                for j in range(f2):
                    if arr_point_helper[j][0] == arr_point[i][0] and arr_point_helper[j][1] == arr_point[i][1]:
                        canvas.itemconfig(arr_point_helper[j][2], fill='white', outline='black', width=2)
                        arr_point_2.append((arr_point_helper[j][0],arr_point_helper[j][1]))
                        
        canvas_poligon = canvas.create_polygon(arr_point_2, outline='#f11',fill='', width=2)
        #раскраска точек

def mouse(event):
    global arr_point_helper
    global canvas_poligon
    global flag
    if event.x < 590 and event.x > 10 and event.y < 590 and event.y > 10:
        if flag != None and len(arr_point_helper) > 0:
            coords.config(text="координаты выбраной точки: " + str(int(event.x)) + ":" + str(int(event.y)))
            if canvas_poligon != None:
                x, y = event.x, event.y
                arr_point_helper[flag[1]][0] = x
                arr_point_helper[flag[1]][1] = y
                canvas.delete(canvas_poligon)
                canvas.coords(flag[0],x - r, y - r, x + r, y + r)
                create_poligon()
            else:
                x, y = event.x, event.y
                arr_point_helper[flag[1]][0] = x
                arr_point_helper[flag[1]][1] = y
                canvas.coords(flag[0],x - r, y - r, x + r, y + r)
        if flag == None:
            coords.config(text="координаты выбраной точки: 0:0")

def delete_all():
    global arr_point_helper
    global canvas_poligon
    if len(arr_point_helper) != 0:
        for a in arr_point_helper:
            canvas.delete(a[2])
        arr_point_helper.clear()
    if canvas_poligon != None:
        canvas.delete(canvas_poligon)
        canvas_poligon = None

def random_create():
    global arr_point_helper
    if entry.get() != "":
        i = 0 
        try:
            i = int(entry.get())
        except:
            msg = "Введено неверное значение"
            mb.showwarning("Предупреждение", msg)
        for j in range(i):
            point = 0
            while point == 0:
                flag_halper = 0
                x = randint(11, 589)
                y = randint(11, 589)
                for a in arr_point_helper:
                    if a[0] == x and a[1] == y:
                        flag_halper = 1
                if flag_halper == 0:
                    id_canvas = canvas.create_oval(x - r, y - r, x + r, y + r , outline="green",fill="green", width=0)
                    canvas.place(x = 0, y = 0)
                    arr_point_helper.append([x,y,id_canvas])
                    point = 1
        create_poligon()
        entry.delete(0, 'end')
    else:
        msg = "Необходимо ввести количество"
        mb.showwarning("Предупреждение", msg)


if __name__ == "__main__":
    win.geometry(str(cv_wid)+"x" + str(cv_hgt))
    window = 10,10,10,590,590,590,590,10
    canvas.create_polygon(window, outline='grey', fill = "white", width=2)
    canvas.bind('<Button-1>', on_click_left_button)
    canvas.bind('<Motion>', mouse)
    canvas.place(x = 0, y = 0)
    btn = Button(win, text="создать полигон", command=create_poligon)
    btn.place(x = 620, y = 10)
    btn = Button(win, text="очистить", command=delete_all)
    btn.place(x = 620, y = 50)
    btn = Button(text="создать точки случайным образом", command=random_create)
    btn.place(x = 620, y = 90)
    label1 = Label(text="Введите количество точек которое необходимо создать", fg="#333", bg="#eee")
    label1.place(x = 620, y = 115)
    entry = Entry()
    entry.place(x = 620, y = 135)
    label1 = Label(text="Для создания точки необходимо нажать ЛКМ", fg="#333", bg="#eee")
    label1.place(x = 620, y = 180)
    label1 = Label(text="Для передвижения необходимо нажать ЛКМ", fg="#333", bg="#eee")
    label1.place(x = 620, y = 195)
    label1 = Label(text="на точку которую необходимо переместить ", fg="#333", bg="#eee")
    label1.place(x = 620, y = 210)
    coords = Label(text="координаты выбраной точки: 0:0", fg="#333", bg="#eee")
    coords.place(x = 620, y = 400)
    win.protocol("WM_DELETE_WINDOW", win.quit)
    win.mainloop()