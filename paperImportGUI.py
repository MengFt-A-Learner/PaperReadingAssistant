# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 13:56:54 2022

@author: MengFt
"""
from PaperDataClass import PaperDataClass
from paperDataSaveInXml import PaperDataXmlFileManagement
import PySimpleGUI as sg
from webbrowser import open_new
from re import split

#%%设定一些变量和方法，用于管理大量的paperDadaClass对象
#已经载入的文章数量
numberPaperExisted=int(0)
#已经读完的文章数量
numberPaperRead=int(0)
#可用的文章数量
numberPaperAvialable=int(0)
existPaperNameList=[]
paperList=[]
currentPaper=PaperDataClass(0)
#定义函数，统计当前共有多少篇文章，用于numberPaperExisted变量的更新
def numberPaperExistedUpdate(tempPaperList):
    numberPaperExisted=len(tempPaperList)    
    return numberPaperExisted
#定义函数，把所有文章的名字统计下来
def existPaperNameListUpdate(tempPaperList):
    existPaperNameList=[]
    for paper in tempPaperList:
        existPaperNameList.append(str(paper.paperId)+" , "+paper.paperName)
    return existPaperNameList

#定义函数，把所有文章的名字格式化出来
def paperNameFormat(tempPaperList):
    paperNameString=""
    for paper in tempPaperList:
        paperNameString+=str(paper.paperId)+", "+paper.paperName+"\n"
    return paperNameString




#%%定义函数，把窗口画出来
def makeWindow(theme):
    #设置初始化的主题
    sg.theme(theme)
    #最上部的功能列表，用于sg.MenubarCustom()设置
    menuDef=[["文件",['创建工程','导入文件','保存文件','导出文件','另存文件(暂不可用)','关闭']],
              ["Help",["关于"]]]
    
    
    #右键换出列表
    rightClickMenuDef=[[],['导出文件','选取文章','刷新','取消','关闭']]
    
    #管理现有文章的界面
    manageWindowLayout=[
        [sg.Text('文章管理系统，用于统计文献阅读情况，辅助文献综述撰写',font='Times 10')],
        [sg.Button("导入文件")],
        [sg.Text('已载入文献数量{}，已读文献数量{}，可用文献数量{}'.format(numberPaperExisted,numberPaperRead,numberPaperAvialable),key='textOfManagePaperNumber',font='Times 15')],
        [sg.Multiline(size=(60,5), expand_x=True, expand_y=True, key='existedPaperName',enable_events=True)]
        ]
    
    #载入新文章的界面
    inputWindowLayout=[
        [sg.Text('文章载入系统，用于载入新的文章',font='Times 10')],
        [sg.Text('已载入文献数量{}'.format(numberPaperExisted),key="textOfPaperExisted",font='Times 15')],
        [sg.Button("选取文章")],
        [sg.Text('文章Id',font='Times 10',size=(8,1)),sg.Input(key='inputPaperId',size=(50,1))],
        [sg.Text('文章名称',font='Times 10',size=(8,1)),sg.Input(key='inputPaperName',size=(50,1),expand_x=True)],
        [sg.Text('文章语言',font='Times 10',size=(8,1)),sg.Combo(values=('中文', '英文'),default_value="中文",size=(10,1),readonly=True,key='inputPaperUsedLanguageMenu')],
        [sg.Button("载入文章")]
        ]
    
    #管理一个文章，详细修改信息的界面
    paperReadingLayout=[
        [sg.Button("选中文献"),sg.Button('确认修改')],
        [sg.Listbox(values = existPaperNameList, 
                    size =(60, 5), key ='existingPaperList',
                    enable_events = True,select_mode = 3)],
        [sg.Text('文章Id',font='Times 10',size=(8,1)),sg.Input(key='currentPaperId',size=(20,1)),
         sg.Text('文章语言',font='Times 10',size=(8,1)),sg.Input(key='currentPaperUsedLanguage',size=(20,1))],
        [sg.Text('文章名称',font='Times 10',size=(8,1)),sg.Input(key='currentPaperName',size=(50,2),expand_x=True)],
        [sg.Text('发表时间',font='Times 10',size=(8,1)),sg.Input(key='currentPaperPublishTime',size=(20,1),expand_x=True),
         sg.Text('发表水平',font='Times 10',size=(8,1)),sg.Combo(values=('顶刊', '顶会','非顶刊SCI1区','SCI2区','SCI3-4区','EI','中文核心'),default_value=None,size=(20,1),readonly=True,key='currentPaperPublicationLevel')],
        [sg.Text('存储路径',font='Times 10',size=(8,1)),
         sg.Input(key='currentPaperFilePath',size=(50,1)),
         sg.Button("打开源文件")],
        [sg.Text('是否可用',font='Times 10',size=(8,1)),
         sg.Combo(values=('未定义', '可用','不可用'),default_value='未定义',size=(20,1),readonly=True,key='currentPaperAvialablity'),
         sg.Text('文章信息录入完成度',font='Times 10',size=(18,1)),
         sg.Input(key='currentPapercompleteness',size=(20,1),expand_x=True)], #是否可用
        [],#文章信息录入完成度
        [sg.Text('文章领域 1级',font='Times 10',size=(11,1)),
         sg.Input(key='currentPaperFiledLevel1',size=(20,1)),
         sg.Text('文章领域 2级',font='Times 10',size=(11,1)),
         sg.Input(key='currentPaperFiledLevel2',size=(20,1)),
         ], #文章领域分类，一级、二级
        [sg.Text('文章主要内容',font='Times 10',size=(8,2)),
         sg.Multiline(size=(60,5), expand_x=True, expand_y=True, key='currentPaperSummary',enable_events=True)], #文章主要内容
        [sg.Text('特点或不足',font='Times 10',size=(8,2)),
         sg.Multiline(size=(60,5), expand_x=True, expand_y=True, key='currentPapercharacteristic',enable_events=True)],#文章特点
        [],#觉得可用的图片(最多两张)
        [],#存储路径
        
        ]
    
    
    #用于打印调试信息的界面
    logging_layout = [[sg.Text("Anything printed will display here!",font='Times 10')],
                      [sg.Multiline(size=(60,15), font='Times 8', expand_x=True, expand_y=True, write_only=True,
                                    reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]
                      ]

    
    layout=[[sg.MenubarCustom(menuDef,key="MENU",font='Times 15',tearoff=True)],]
    layout+=[[sg.TabGroup([[sg.Tab("文献管理",manageWindowLayout)],
                           [sg.Tab("文献载入",inputWindowLayout)],
                           [sg.Tab("详细信息",paperReadingLayout)],
                           [sg.Tab('调试信息', logging_layout)]])        
        ]]
    layout[-1].append(sg.Sizegrip())

    window=sg.Window('阅读文献小助手(撰写综述中...)_V1.0',
                     layout,
                     right_click_menu=rightClickMenuDef,
                     right_click_menu_tearoff=True,
                     grab_anywhere=True,
                     resizable=True, 
                     margins=(0,0), 
                     use_custom_titlebar=True, 
                     finalize=True, 
                     keep_on_top=True,
                     return_keyboard_events=True)
    window.set_min_size(window.size)
    return window

#%%定义一些函数，用于界面的及时更新和交互处理
#更新一些计数的信息，右键刷新的时候会调用这个函数
def windowPaperDataListUpdateFromBackenup(window,backenUpProject):
    global numberPaperExisted
    global numberPaperRead
    global numberPaperAvialable            
    global paperList
    paperList=backenUpProject.paperDataList
    #更新numberPaperExisted数据
    numberPaperExisted=len(paperList)
    #更新numberPaperAvialable
    numberPaperAvialable=0
    for paper in paperList:
        print(paper.paperName)
        if paper.Availability==1:
            numberPaperAvialable+=1    
    windowNumberUpdate(window)
    
def windowNumberUpdate(window):
    global numberPaperExisted
    global numberPaperRead
    global numberPaperAvialable            
    window['textOfManagePaperNumber'].update('已载入文献数量{}，已读文献数量{}，可用文献数量{}'.format(numberPaperExisted,numberPaperRead,numberPaperAvialable))
    window['textOfPaperExisted'].update('已载入文献数量{}'.format(numberPaperExisted))
    
    window['existedPaperName'].update(paperNameFormat(paperList))
    #window['existingPaperList'].TKListbox.delete(0, 'end')
    window['existingPaperList'].update(values=None)
    window['existingPaperList'].update(values=existPaperNameListUpdate(paperList))
    window['inputPaperId'].update(value="")
    window['inputPaperName'].update(value="")



#初始化当前编辑文章的相关信息，在“详细信息”界面的“选中文献”按键调用
def windowCurrentPaperDataInit(tempWindow,tempPaper):
    tempWindow['currentPaperId'].update(tempPaper.paperId)
    tempWindow['currentPaperName'].update(tempPaper.paperName)
    tempWindow['currentPaperUsedLanguage'].update(tempPaper.languageList[tempPaper.paperUsedLanguage])
    tempWindow['currentPaperPublicationLevel'].update(tempPaper.publicationLevel)
    tempWindow['currentPaperAvialablity'].update(tempPaper.Availability)
    tempWindow['currentPaperFilePath'].update(tempPaper.paperFilePath)
    tempWindow['currentPaperFiledLevel1'].update(tempPaper.fieldLevel1)
    tempWindow['currentPaperFiledLevel2'].update(tempPaper.fieldLevel2)
    tempWindow['currentPaperSummary'].update(tempPaper.summaryReExtract)
    tempWindow['currentPapercharacteristic'].update(tempPaper.characteristic)
    tempWindow['currentPapercompleteness'].update(tempPaper.completeness)
    
    

#更新当前编辑文章的相关信息，在“详细信息”界面的“确认修改”按键调用
#将window上编写的信息，保存到后台的paperList的相应元素中
def windowCurrentPaperDataUpdate(tempWindow,tempPaper):
    #tempId=tempWindow['currentPaperId'].get()
    tempName=tempWindow['currentPaperName'].get()
    tempLanguage=tempWindow['currentPaperUsedLanguage'].get()
    tempPublishedTime=tempWindow['currentPaperPublishTime'].get()
    tempPublishedLevel=tempWindow['currentPaperPublicationLevel'].get()
    #print(tempName,tempLanguage,tempPublishedTime,tempPublishedLevel)
    tempPaperAvialablity=tempWindow['currentPaperAvialablity'].get()
    tempPaperFieldLevel1=tempWindow['currentPaperFiledLevel1'].get()
    tempPaperFieldLevel2=tempWindow['currentPaperFiledLevel2'].get()
    tempPaperSummary=tempWindow['currentPaperSummary'].get()
    tempPapercharacteristic=tempWindow['currentPapercharacteristic'].get()
    tempPaper.updatePaperName(tempName)
    tempPaper.updatePaperUsedLanguage(tempLanguage)
    tempPaper.updatePublishedTime(tempPublishedTime)
    tempPaper.updatePublicationLevel(tempPublishedLevel)
    print("传入Avialablity为：{},数据类型为：{}".format(tempPaperAvialablity,type(tempPaperAvialablity)))
    tempPaper.updateAvialablity(str(tempPaperAvialablity))
    print("保存的Avialablity为：",tempPaper.Availability)
    tempPaper.updateFieldLevel1(tempPaperFieldLevel1)
    tempPaper.updateFieldLevel2(tempPaperFieldLevel2)
    tempPaper.updatePaperSummary(tempPaperSummary)
    tempPaper.updatePapercharacteristic(tempPapercharacteristic)
    tempPaper.paperDataOutput()
    
#%%定义一些变量和函数，用于后端存储和管理
currentBackendProject=PaperDataXmlFileManagement("尚未定义工程")
#创建一个工程
def backendCreatNewProject(window,fileName,filePath):
    print("创建一个新工程")
    #window.
    currentBackendProject=PaperDataXmlFileManagement(fileName,filePath)
    
    return currentBackendProject
    
#%%定义界面运行的主函数，主要是逻辑，应对所有事件的反应
def main():
    window = makeWindow(sg.theme())
    global numberPaperExisted
    global numberPaperRead
    global numberPaperAvialable            
    global currentBackendProject
    global paperList
    
    #定义一组变量，用于快捷键操作
    keyboardSaveFlag=False   #用于组合判断ctrl+s组合
    

    # 时间循环操作
    while True:
        event,values=window.read(timeout=100)
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break  
        if event not in ("__TIMEOUT__","MouseWheel:Up","MouseWheel:Down"):
            print("event=",event)
        if event in ('创建工程'):
            xmlFilePath = sg.popup_get_folder('选取保存路径', keep_on_top=True)
            if xmlFilePath==None:
                sg.popup("取消选择",font='Times 15',keep_on_top=True)
                continue
            #sg.popup("You chose: " + str(xmlFilePath), keep_on_top=True)
            xmlFileName=sg.popup_get_text("输入工程名（无需后缀）",keep_on_top=True)
            currentBackendProject=backendCreatNewProject(window,xmlFileName,xmlFilePath)
        if event in ('保存文件'):
            try:
                #先判断一下是否已经定义了工程文件
                if currentBackendProject.xmlFilePath in("尚未定义工程.xml",""):
                    sg.popup("尚未定义有工程文件",font='Times 15',keep_on_top=True)
                    print("尚未定义有工程文件")
                    continue
                #保存一下文件
                for paperData in paperList:                
                    currentBackendProject.inputPaperData(paperData)    
            except Exception as err:
                print(err)
                #sg.popup("错误信息："+err,font='Times 15',keep_on_top=True)
                sg.popup("尚未有工程文件被初始化",font='Times 15',keep_on_top=True)
                print("尚未有工程文件被初始化")
                continue
        
        if event in ('导出文件'):
            try:
                #先判断一下是否已经定义了工程文件
                if currentBackendProject.xmlFilePath in("尚未定义工程.xml",""):
                    sg.popup("尚未定义有工程文件",font='Times 15',keep_on_top=True)
                    print("尚未定义有工程文件")
                    continue
                #保存一下文件
                for paperData in paperList:                
                    currentBackendProject.inputPaperData(paperData)    
            except Exception as err:
                print(err)
                #sg.popup("错误信息："+str(err),font='Times 15',keep_on_top=True)
                sg.popup("尚未有工程文件被初始化",font='Times 15',keep_on_top=True)
                print("尚未有工程文件被初始化")
                continue
            currentBackendProject.saveXmlFile()
            print("导出了文件，名为",currentBackendProject.xmlFilePath)
        if event in ('导入文件'):
            inputXmlFilePath=sg.popup_get_file("选取数据库XML文件",keep_on_top=True)
            if inputXmlFilePath==None:
                sg.popup("取消选择",font='Times 15',keep_on_top=True)
                continue
            if inputXmlFilePath.endswith(".xml"):
                #newXmlFilePath = sg.popup_get_folder('选取保存路径', keep_on_top=True,default_path='D:\Mirror\沉头孔测量方法与加工误差分析综述\综述撰写辅助脚本\\')
                #处理引入xml文件的全局名，提取其存储位置，用于输出文件地址的默认值
                print("inputXmlFilePath=",inputXmlFilePath)
                tempOutputFilePathList=split(r'[/]',inputXmlFilePath)
                tempOutputFilePath=""
                if len(tempOutputFilePathList)>=1:  
                    for i in range(0,len(tempOutputFilePathList)-1):
                        tempOutputFilePath+=tempOutputFilePathList[i]+"/"

                else:
                    print("inputXmlFilePathList为空")
                    continue
                #弹出对话框，用于选择输出文件的保存位置，默认值是输入文件的全局路径
                newXmlFilePath = sg.popup_get_folder('选取保存路径', keep_on_top=True,default_path=tempOutputFilePath)
                #处理一下这个流程的异常返回情况
                if newXmlFilePath==None:
                    sg.popup("取消选择",font='Times 15',keep_on_top=True)    
                    continue
                tempXmlName=split(r'[/.]',inputXmlFilePath)[-2]
                print("tempXmlName=",tempXmlName)
                newXmlFileName=sg.popup_get_text("输入工程名（无需后缀）",keep_on_top=True,default_text=tempXmlName)
                if newXmlFileName in (None,""):
                    print("未输入有效的文件名")
                    continue
                currentBackendProject=backendCreatNewProject(window,newXmlFileName,newXmlFilePath)
                print("选中了文件：{}，即将导入".format(inputXmlFilePath))
                currentBackendProject.readTreeFromXmlFile(inputXmlFilePath)
                print("成功导入文件{}，包含文章{}篇".format(newXmlFileName,len(currentBackendProject.paperDataList)))
                #把后台的paperDataList 传入到window用的paperList，并更新一些基本参数
                windowPaperDataListUpdateFromBackenup(window,currentBackendProject)
            else:
                print("导入文件出错：文件后缀错误")
                

                
        
        if event  in ('关闭',sg.WIN_CLOSED):
            break
        if event in ('刷新'):
            windowNumberUpdate(window)
            #window['textOfManagePaperNumber'].Update('已载入文献数量{}，已读文献数量{}，可用文献数量{}'.format(numberPaperExisted,numberPaperRead,numberPaperAvialable))
            #window['textOfPaperExisted'].Update('已载入文献数量{}'.format(numberPaperExisted))
        if event in ("选取文章"):
            print("点击按钮，选取文章")
            paperFilePath=sg.popup_get_file('选取文章', keep_on_top=True)
            #global numberPaperExisted     

            if paperFilePath==None:
                sg.popup("取消选择",font='Times 15',keep_on_top=True)
            else:
                paperList.append(PaperDataClass(numberPaperExisted))
                paperList[numberPaperExisted].setFilePath(paperFilePath)
                paperFilePathSplitList=str.split(paperFilePath,'/')
                window['inputPaperId'].update(numberPaperExisted)
                window['inputPaperName'].update(paperFilePathSplitList[-1])
                
        if event in ("载入文章"):
            print("文章确认无误，开始载入")

            tempPaperName=window['inputPaperName'].get()
            tempPaperLanguage=window['inputPaperUsedLanguageMenu'].get()
            if tempPaperName in ('',None):
                sg.popup("文章名为空",font='Times 15',keep_on_top=True)
                continue
            if tempPaperLanguage in ('',None):
                sg.popup("所用语言尚未定义",font='Times 15',keep_on_top=True)
                continue
            paperList[numberPaperExisted].updatePaperName(tempPaperName)
            paperList[numberPaperExisted].updatePaperUsedLanguage(tempPaperLanguage)
            paperList[numberPaperExisted].paperDataOutput()
            numberPaperExisted+=1
            windowNumberUpdate(window)
            #global numberPaperExisted    
        if event in ("选中文献"):
            paperNameString=window['existingPaperList'].get()
            if paperNameString==[]:
                sg.popup("尚未选中文献",font='Times 15',keep_on_top=True)
                continue
            print("选中文献：",paperNameString)
            tempPaperId=int(str.split(paperNameString[0],',')[0])
            currentPaper=paperList[tempPaperId]
            windowCurrentPaperDataInit(window,currentPaper)
        if event in ("确认修改"):
            paperNameString=window['existingPaperList'].get()
            tempPaperId=int(str.split(paperNameString[0],',')[0])
            currentPaper=paperList[tempPaperId]
            windowCurrentPaperDataUpdate(window,currentPaper)
        if event in ("打开源文件"):
            #从窗口读取“文章id"
            tempId=int(window['currentPaperId'].get())
            #从窗口读取Paper Path，用于打开文件
            tempPaperPath=window['currentPaperFilePath'].get()
            if tempPaperPath.endswith(".pdf"):
                 #paperList[tempId].paperFilePath=tempPaperPath
                 open_new(tempPaperPath)
                 #window["currentPaperFilePath"].update(tempPaperPath)
            else :
                tempPaperPath=sg.popup_get_file("重新定义文件路径",title="文件路径不存在",keep_on_top=True)
                if tempPaperPath.endswith(".pdf"):
                     paperList[tempId].paperFilePath=tempPaperPath
                     open_new(tempPaperPath)
                     window["currentPaperFilePath"].update(tempPaperPath)
                    
                else: 
                    print("tempPaperPath=",tempPaperPath)
                    #sg.popup("取消：定义文件路径")
                    window["currentPaperFilePath"].update("")
                    continue
            
            print("打开源文件，路径为",)
        #快捷键时间反馈
        keyboardCallBackDict={"ESC":"Escape:27",
                              "leftCtrl":"Control_L:17",
                              "rightCtrl":"Control_R:17",
                              "enter":"\r",
                              "TAB":"",
                              "shift":"Shift_L:16"}
        if event in (keyboardCallBackDict["ESC"]):
            print("按键触发ESC")    
        if event in (keyboardCallBackDict["leftCtrl"],keyboardCallBackDict["rightCtrl"]):
            print("按键触发CTRL")    
            keyboardSaveFlag=True
        if event in ('s'):
            if keyboardSaveFlag==True:
                print("保存")
                try:
                    #先判断一下是否已经定义了工程文件
                    if currentBackendProject.xmlFilePath in("尚未定义工程.xml",""):
                        sg.popup("尚未定义有工程文件",font='Times 15',keep_on_top=True)
                        print("尚未定义有工程文件")
                        continue
                    #保存一下文件
                    print("当前后台文章数量:",len(currentBackendProject.paperDataList))
                    print("当前前台文章数量:",len(paperList))
                    for paperData in paperList:                
                        currentBackendProject.inputPaperData(paperData)    
                except Exception as err:
                    print("错误信息：",err)
                    #sg.popup("错误信息："+err,font='Times 15',keep_on_top=True)
                    print("尚未有工程文件被初始化")
                    continue
                currentBackendProject.saveXmlFile()

                print("保存文件名为",currentBackendProject.xmlFilePath)

            else : keyboardSaveFlag=False
        if event in (keyboardCallBackDict["enter"]):
            print("按键触发enter")    
        if event in (keyboardCallBackDict["TAB"]):
            print("按键触发TAB")    
        if event in (keyboardCallBackDict["shift"]):
            print("按键触发shift")    

    window.close()
    
    
if __name__ == '__main__':
    sg.theme('python')
    # sg.theme('DefaultNoMoreNagging')
    main()




