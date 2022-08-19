# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 21:14:45 2022

@author: MengFt
"""

import PySimpleGUI as sg

#设置界面主题
sg.theme("DarkAmber")

#定义窗口布局
layout=[[sg.Text("this is Row 1")],
        [sg.Text("write something in Row 2"),sg.InputText()],
        [sg.Button("ok"),sg.Button("cancle")]]        

#定义窗口对象
window=sg.Window("window title",layout)

#循环事件，获取输入值
while True:
    event,values=window.Read()
    if event in (None,'cancle'):
        break
    print("you input ",values[0])
    
window.close()

    
    
