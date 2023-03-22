from tkinter import *
from scipy.linalg import solve
import numpy as np
import math
import tkinter.messagebox as mb

c_btn = 0
ac_btn = 0
hp_btn = 0
np_btn = 0
one_btn = 0
two_btn = 0
coords = 0
opred = 0
opred1 = 0
arr_point_helper = []
canvas_poligon = []
cyclicity = True
norm_param = False
parad_glad = 1
flag = None
win = Tk()
win.title("Исследование существования и построение циклических и ациклических интерполяционных линий")
cv_wid = 950
cv_hgt = 600
r = 6
number_point = 1
canvas = Canvas(win, width=cv_wid, height=cv_hgt, borderwidth=1,highlightthickness=0)

#метод эрмита для циклической интерполяции
def get_Hermite_c(input):
    global cyclicity
    global norm_param
    global parad_glad
    #определение количества строчек
    n = len(input) + parad_glad
    m = len(input)
    #определение Pn
    if norm_param:
        Pn = []
        for i in range(m):
            Pn.append(i)
    else:
        d = 0
        for i in range(1,m, 1):
            d += math.sqrt(((input[i][0] - input[i - 1][0]) ** 2) + ((input[i][1] - input[i - 1][1]) ** 2))
        uk = [0]
        for i in range(1,m, 1):
            uk.append(uk[len(uk)-1] + ((math.sqrt(((input[i][0] - input[i - 1][0]) ** 2) + ((input[i][1] - input[i - 1][1]) ** 2)))/d))
        Pn = uk
    #определение X,Y
    X = []
    Y = []
    for i in input:
        X.append(i[0])
        Y.append(i[1])
    
    X.append(0)
    Y.append(0)
    if parad_glad == 2:
        Y.append(0)
        X.append(0)
    
    ###########################################
    pn = []
    for j in Pn:
        pn_helper = []
        for i in reversed(range(n)):
            pn_helper.append(j ** i)
        pn.append(pn_helper)
    #################################
    pn_helper = []
    for i in reversed(range(n)):
        if i > 0:
            if cyclicity:
                pn_helper.append(((Pn[0] ** (i - 1)) - (Pn[len(Pn)-1] ** (i - 1))) * i)
            else:
                pn_helper.append(((Pn[0] ** (i - 1)) + (Pn[len(Pn)-1] ** (i - 1))) * i)
    while len(pn_helper) != n:
        pn_helper.append(0)
    pn.append(pn_helper)
    #################################
    if parad_glad == 2:
        pn_helper = []
        for i in reversed(range(n)):
            if i - 1 > 0:
                if cyclicity:
                    pn_helper.append(((Pn[0] ** (i - 2)) - (Pn[len(Pn)-1] ** (i - 2))) * i * (i - 1))
                else:
                    pn_helper.append(((Pn[0] ** (i - 2)) + (Pn[len(Pn)-1] ** (i - 2))) * i * (i - 1))
        while len(pn_helper) != n:
            pn_helper.append(0)
        pn.append(pn_helper)
    ###########################################
    p = np.array(pn)
    Y = np.array(Y).reshape((len(Y), 1))
    X = np.array(X).reshape((len(X), 1))
    print(p)
    opred.config(text="определитель = " + str(np.linalg.det(p)))
    
    #проверка всех условий
    helper_flag = 0
    if parad_glad == 1:
        if cyclicity:
            if norm_param:
                if (len(input) % 2 == 1):
                    msg = "параметрические длины равны, количество точек нечетное\nопределитель = 0"
                    mb.showwarning("Предупреждение", msg)
                    helper_flag = 1
            else:
                if np.linalg.det(p) == 0:
                    msg = "параметрические длины равны, количество точек нечетное\nопределитель = 0"
                    mb.showwarning("Предупреждение", msg)
                    helper_flag = 1
        else:
            if norm_param:
                if (len(input) % 2 == 0):
                    msg = "параметрические длины между двумя крайними точками равно, \nколичество точек четное\nопределитель = 0"
                    mb.showwarning("Предупреждение", msg)
                    helper_flag = 1
            else:
                if np.linalg.det(p) == 0:
                    msg = "параметрические длины между двумя крайними точками равно, \nколичество точек четное\nопределитель = 0"
                    mb.showwarning("Предупреждение", msg)
                    helper_flag = 1
    #Создание функции
    if helper_flag == 0:
        opred1.config(text="")
        x = solve(p, X)
        y = solve(p, Y)
        def res(n):
            i = 0
            x_itog = 0
            for x_helper in reversed(x):
                x_itog += x_helper[0] * (n ** i)
                i = i + 1
            y_itog = 0
            i= 0
            for y_helper in reversed(y):
                y_itog += y_helper[0] * (n ** i)
                i = i + 1
            return x_itog, y_itog
        return res


def on_click_left_button(event):
    global arr_point_helper
    global number_point
    x, y = event.x, event.y
    r = 6
    if x>10 and y>10 and x<590 and y<590:
        flag_helper = 0
        i = 0
        for a in arr_point_helper:
            if (x-a[0])**2 + (y-a[1])**2 - (r+2)**2 < 0:
                flag_helper = 1
                id = a[2]
                id_2 = a[3]
                j = i
            i = i + 1
        if flag_helper == 0:
            id_canvas = canvas.create_oval(x - r, y - r, x + r, y + r , outline="green",fill="green", width=0)
            id_canvas2 = canvas.create_text(x,y-14,text="P" + str(number_point))
            number_point = number_point + 1
            canvas.place(x = 0, y = 0)
            arr_point_helper.append([x,y,id_canvas,id_canvas2])
        else:
            global flag
            if flag == None:
                flag = id,j,id_2
            else:
                flag = None
    interpolation()

def interpolation():
    global norm_param
    global arr_point_helper
    global canvas_poligon
    global cyclicity
    if canvas_poligon != []:
        for i in canvas_poligon:
            canvas.delete(i)
        canvas_poligon.clear()
    if len(arr_point_helper) > 2:
        arr_point_x = []
        arr_point_y = []
        arr_point = []
        for a in arr_point_helper:
            arr_point_x.append(a[0])
            arr_point_y.append(a[1])
            arr_point.append((a[0], a[1]))
        x = arr_point_x
        y = arr_point_y

        f  = get_Hermite_c(arr_point)
        if f != None:
            if norm_param:
                xnew = np.linspace(0, len(arr_point) - 1, 200)
            else:
                xnew = np.linspace(0, 1, 200)
            ynew = []
            for a in xnew:
                ynew.append(f(a))
            line = []
            i = 0
            for x2 in xnew:
                res = f(x2)
                line.append(res[0])
                line.append(res[1])
            i = 0
            for l in line:
                if (i % 2 == 0) and (i + 3 <= len(line) - 1) and (10 <= line[i+2] <= 590) and (10 <= line[i+3] <= 590) and (10 <= line[i] <= 590) and (10 <= line[i+1] <= 590):
                    canvas_poligon.append(canvas.create_line((line[i],line[i+1],line[i+2],line[i+3],),fill='#f11', width=2))
                i+=1


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
                canvas.coords(flag[0],x - r, y - r, x + r, y + r)
                canvas.coords(flag[2],x, y - 14)
                interpolation()
            else:
                x, y = event.x, event.y
                arr_point_helper[flag[1]][0] = x
                arr_point_helper[flag[1]][1] = y
                canvas.coords(flag[0],x - r, y - r, x + r, y + r)
                canvas.coords(flag[2],x, y - 14)
        if flag == None:
            coords.config(text="координаты выбраной точки: 0:0")

def delete_all():
    global arr_point_helper
    global canvas_poligon
    global number_point
    if len(arr_point_helper) != 0:
        for a in arr_point_helper:
            canvas.delete(a[2])
            canvas.delete(a[3])
            number_point = 1
        arr_point_helper.clear()
    if canvas_poligon != []:
        for i in canvas_poligon:
            canvas.delete(i)
        canvas_poligon.clear()

def create_cyclic_interpolation():
    global cyclicity
    global c_btn
    global ac_btn
    cyclicity = True
    c_btn.configure(state=DISABLED)
    ac_btn.configure(state=NORMAL)
    interpolation()

def create_acyclic_interpolation():
    global cyclicity
    global c_btn
    global ac_btn
    cyclicity = False
    c_btn.configure(state=NORMAL)
    ac_btn.configure(state=DISABLED)
    interpolation()

def hord_param_def():
    global norm_param
    global hp_btn
    global np_btn
    norm_param = False
    hp_btn.configure(state=DISABLED)
    np_btn.configure(state=NORMAL)
    interpolation()

def norm_param_def():
    global norm_param
    global hp_btn
    global np_btn
    norm_param = True
    hp_btn.configure(state=NORMAL)
    np_btn.configure(state=DISABLED)
    interpolation()

def one_glad_def():
    global parad_glad
    global one_btn
    global two_btn
    parad_glad = 1
    two_btn.configure(state=NORMAL)
    one_btn.configure(state=DISABLED)
    interpolation()

def two_glad_def():
    global parad_glad
    global one_btn
    global two_btn
    parad_glad = 2
    one_btn.configure(state=NORMAL)
    two_btn.configure(state=DISABLED)
    interpolation()

if __name__ == "__main__":
    win.geometry(str(cv_wid)+"x" + str(cv_hgt))
    window = 10,10,10,590,590,590,590,10
    canvas.create_polygon(window, outline='grey', fill = "white", width=2)
    canvas.bind('<Button-1>', on_click_left_button)
    canvas.bind('<Motion>', mouse)
    canvas.place(x = 0, y = 0)
    c_btn = Button(win, text="циклическая интерполяция", command=create_cyclic_interpolation, state=DISABLED)
    c_btn.place(x = 620, y = 10)
    ac_btn = Button(win, text="ациклическая интерполяция", command=create_acyclic_interpolation)
    ac_btn.place(x = 620, y = 50)
    hp_btn = Button(win, text="хордовая параметризация", command=hord_param_def, state=DISABLED)
    hp_btn.place(x = 620, y = 90)
    np_btn = Button(win, text="нормализованная параметризация", command=norm_param_def)
    np_btn.place(x = 620, y = 130)
    one_btn = Button(win, text="первый прядок гладкости", command=one_glad_def, state=DISABLED)
    one_btn.place(x = 620, y = 170)
    two_btn = Button(win, text="второй порядок гладкости", command=two_glad_def)
    two_btn.place(x = 620, y = 210)
    btn = Button(win, text="очистить", command=delete_all)
    btn.place(x = 620, y = 250)
    opred = Label(text="определитель = ", fg="#333", bg="#eee")
    opred.place(x = 620, y = 290)
    opred1 = Label(text="", fg="#333", bg="#eee")
    opred1.place(x = 620, y = 330)
    label1 = Label(text="интерполяция возможна от 3 точек", fg="#333", bg="#eee")
    label1.place(x = 620, y = 370)
    coords = Label(text="координаты выбраной точки: 0:0", fg="#333", bg="#eee")
    coords.place(x = 620, y = 490)
    win.protocol("WM_DELETE_WINDOW", win.quit)
    win.mainloop()