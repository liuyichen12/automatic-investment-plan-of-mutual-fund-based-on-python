import tkinter as tk
import tkinter.messagebox
import jjkshz
import kline
import zhineng
root = tk.Tk()
root.title("基金定投计算器")
root.geometry('460x250')
v1 = tk.StringVar()
v2 = tk.StringVar()
v3 = tk.StringVar()
v5 = tk.StringVar()
v6 = tk.StringVar()
# v5.set("格式：")
OPTIONS1 = [
    "每周",
    "每两周",
    "每月"
]
v3.set(OPTIONS1[0])
v4 = tk.IntVar()
WAY = [
    ("普通定投", 0),
    ("智能定投", 1)
]
v4.set(0)
label1 = tk.Label(root, text="欢迎使用基金定投计算器")
label1.grid(row=0, columnspan=3)
label2 = tk.Label(root, text="定投基金代码：")
label2.grid(row=1, column=0)
entry1 = tk.Entry(root, textvariable=v1, width=40)
entry1.grid(row=1, column=1,columnspan=2)
label3 = tk.Label(root, text="定投金额：")
label3.grid(row=2, column=0)
entry2 = tk.Entry(root, textvariable=v2, width=40)
entry2.grid(row=2, column=1,columnspan=2)
label4 = tk.Label(root, text="定投周期：")
label4.grid(row=3, column=0)
optionmenu1 = tk.OptionMenu(root, v3, *OPTIONS1)
optionmenu1.grid(row=3, column=1,columnspan=2)
for way, num in WAY:
    b = tk.Radiobutton(root, text=way, variable=v4, value=num)
    b.grid(row=4, column=num)
label6 = tk.Label(root, text="开始时间：")
label6.grid(row=5, column=0)
entry3 = tk.Entry(root, textvariable=v5, width=40)
entry3.grid(row=5, column=1,columnspan=2)
label7 = tk.Label(root, text="截止时间：")
label7.grid(row=6, column=0)
entry4 = tk.Entry(root, textvariable=v6, width=40)
entry4.grid(row=6, column=1,columnspan=2)


def show1():
    # if float(v5.get()) > float(v6.get()):
    # tkinter.messagebox.showerror("出错啦", "开始时间应该早于截止时间")
    # else:
    if v4.get() == 0:
        if v3.get() == "每周":
            option = 1
        if v3.get() == "每两周":
            option = 2
        if v3.get() == "每月":
            option = 3
    kline.Kline(float(v2.get()), v1.get(), float(v5.get()), float(v6.get()), option)


def show2():
    if float(v5.get()) > float(v6.get()):
        tkinter.messagebox.showerror("出错啦", "开始时间应该早于截止时间")
    else:
        if v4.get() == 0:
            if v3.get() == "每周":
                option = 1
            if v3.get() == "每两周":
                option = 2
            if v3.get() == "每月":
                option = 3
            jjkshz.CL(float(v2.get()), v1.get(), float(v5.get()), float(v6.get()), option)

        if v4.get() == 1:
            if v3.get() == "每周":
                option = 1
            if v3.get() == "每两周":
                option = 2
            if v3.get() == "每月":
                option = 3
            zhineng.junxianDT(float(v2.get()), v1.get(), float(v5.get()), float(v6.get()), option)


button1 = tk.Button(root, text="查看K线图", width=20, command=show1)
button1.grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)
button2 = tk.Button(root, text="查看收益图", width=20, command=show2)
button2.grid(row=7, column=1, sticky=tk.E, padx=10, pady=5)


def create():
    top = tk.Toplevel()
    top.title("基金收益排行榜")
    dict1 = jjkshz.read_excel()
    newlabel1 = tk.Label(top, text="基金收益排行榜")
    newlabel1.grid(row=0, columnspan=3)
    newlabel2 = tk.Label(top, text="NO.1 :")
    newlabel2.grid(row=1, column=0)
    newlabel3 = tk.Label(top, text=dict1[0][0])
    newlabel3.grid(row=1, column=1)
    newlabel4 = tk.Label(top, text=dict1[0][1])
    newlabel4.grid(row=1, column=2)
    newlabel5 = tk.Label(top, text="NO.2 :")
    newlabel5.grid(row=2, column=0)
    newlabel6 = tk.Label(top, text=dict1[1][0])
    newlabel6.grid(row=2, column=1)
    newlabel7 = tk.Label(top, text=dict1[1][1])
    newlabel7.grid(row=2, column=2)
    newlabel8 = tk.Label(top, text="NO.3 :")
    newlabel8.grid(row=3, column=0)
    newlabel9 = tk.Label(top, text=dict1[2][0])
    newlabel9.grid(row=3, column=1)
    newlabel10 = tk.Label(top, text=dict1[2][1])
    newlabel10.grid(row=3, column=2)
    newlabel11 = tk.Label(top, text="NO.4 :")
    newlabel11.grid(row=4, column=0)
    newlabel12 = tk.Label(top, text=dict1[3][0])
    newlabel12.grid(row=4, column=1)
    newlabel13 = tk.Label(top, text=dict1[3][1])
    newlabel13.grid(row=4, column=2)
    newlabel14 = tk.Label(top, text="NO.5 :")
    newlabel14.grid(row=5, column=0)
    newlabel15 = tk.Label(top, text=dict1[4][0])
    newlabel15.grid(row=5, column=1)
    newlabel16 = tk.Label(top, text=dict1[4][1])
    newlabel16.grid(row=5, column=2)
    newlabel17 = tk.Label(top, text="NO.6 :")
    newlabel17.grid(row=6, column=0)
    newlabel18 = tk.Label(top, text=dict1[5][0])
    newlabel18.grid(row=6, column=1)
    newlabel19 = tk.Label(top, text=dict1[5][1])
    newlabel19.grid(row=6, column=2)
    newlabel20 = tk.Label(top, text="NO.7 :")
    newlabel20.grid(row=7, column=0)
    newlabel21 = tk.Label(top, text=dict1[6][0])
    newlabel21.grid(row=7, column=1)
    newlabel22 = tk.Label(top, text=dict1[6][1])
    newlabel22.grid(row=7, column=2)
    newlabel23 = tk.Label(top, text="NO.8 :")
    newlabel23.grid(row=8, column=0)
    newlabel24 = tk.Label(top, text=dict1[7][0])
    newlabel24.grid(row=8, column=1)
    newlabel25 = tk.Label(top, text=dict1[7][1])
    newlabel25.grid(row=8, column=2)
    newlabel26 = tk.Label(top, text="NO.9 :")
    newlabel26.grid(row=9, column=0)
    newlabel27 = tk.Label(top, text=dict1[8][0])
    newlabel27.grid(row=9, column=1)
    newlabel28 = tk.Label(top, text=dict1[8][1])
    newlabel28.grid(row=9, column=2)
    newlabel29 = tk.Label(top, text="NO.10 :")
    newlabel29.grid(row=10, column=0)
    newlabel30 = tk.Label(top, text=dict1[9][0])
    newlabel30.grid(row=10, column=1)
    newlabel31 = tk.Label(top, text=dict1[9][1])
    newlabel31.grid(row=10, column=2)


tk.Button(root, text="查看排行榜", command=create).grid(row=7, columnspan=2)
root.mainloop()
