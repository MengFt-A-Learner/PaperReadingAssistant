# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 11:38:16 2022

@author: MengFt
"""
from PaperDataClass import PaperDataClass
import PySimpleGUI as sg
from paperDataSaveInXml import paperAssistConfigManager,PaperDataXmlFileManagement
from re import split
from webbrowser import open_new
import time
class PaperImportGui2(object):
    def __init__(self):
        print("一个文献编辑窗口被实例化")
        #定义一些变量：
        #1.前台变量
        ##统计前台有多少文献
        self.numberPaperExisted=0
        ##统计前台已读多少文献（根据完成度判断并统计）
        self.numberPaperRead=0
        ##统计前台有多少可引用文献(根据可用性判断并统计)
        self.numberPaperAvialable=0
        ##前台列表，在保存的时候从前台更新到后台；读取或初始化时从后台更新给前台列表
        self.paperListFrontEnd=[]
        ##当前要使用或正在使用的文章对象
        self.currentPaper=PaperDataClass(0)
        ##现有文章的全部名称列表
        self.existPaperNameList=[] 
        ##提前初始化一个paper对象，是编辑文章详细信息时要使用的对象，提前赋id为-1，到时候好判断
        self.currentPaperManaged=PaperDataClass(-1)
        ##快捷键时间反馈对应的字典
        self.keyboardCallBackDict={"ESC":"Escape:27",
                              "leftCtrl":"Control_L:17",
                              "rightCtrl":"Control_R:17",
                              "enter":"\r",
                              "TAB":"",
                              "shift":"Shift_L:16"}

        #2.后台变量
        ##后台使用的文章列表，在保存的时候从前台更新到后台；读取或初始化时从后台更新给前台列表
        self.paperListBackEnd=[]
        ##后台的文件存储绝对路径
        self.xmlFilePath=""
        ##后台文件管理对象
        self.currentBackendProject=PaperDataXmlFileManagement()
        #3.系统变量
        ##记录相对路径安全文件夹的地址
        self.safeFolderPath=""+"./configFolder/"
        ##记录环境配置变量的路径和文件名
        self.configFilePathName=""+"./configFile.xml"
        ##初始化文件管理类型
        self.configFileManager=paperAssistConfigManager(self.safeFolderPath,self.configFilePathName)
        ##记录配置文件读取成功的标志位
        self.flagConfigFileRead=0
        ##记录窗口是否已经开启
        self.flagWindowCreate=False
        ##记录是否有xml文件被激活
        self.flagXmlFileAvialable=False
        ##记录当前文献保存的情况
        self.flagCurrentPaperSave=0
        ##记录使用快捷键触发的整个工程文件的保存情况，是ctrl+s的中间保持flag
        self.keyboardSaveFlag=False
        
    def projectInitFromConfigFile(self):
        print("读取配置文件")
        #将配置文件读取结果更新进标志位
        self.flagConfigFileRead=self.configFileManager.configFileInput()
        
    def windowLayoutInit(self):
        #设置初始化的主题
        sg.theme("Dark")
        #最上部的功能列表，用于sg.MenubarCustom()设置
        self.menuDef=[["文件",['创建工程','导入文件','保存文件','导出文件','另存文件(暂不可用)','关闭']],
                  ["配置",["保存配置文件","清理配置文件"]],
                      ["Help",["关于"]]]
        #右键换出列表
        self.rightClickMenuDef=[[],['导出文件','选取文章','刷新','取消','关闭']]
        #管理现有文章的界面
        manageWindowLayout=[
            [sg.Text('文章管理系统，用于统计文献阅读情况，辅助文献综述撰写',font='Times 10')],
            [sg.Button("导入文件")],
            [sg.Text('已载入文献数量{}，已读文献数量{}，可用文献数量{}'
                     .format(self.numberPaperExisted,self.numberPaperRead,self.numberPaperAvialable),
                     key='textOfManagePaperNumber',font='Times 15')],
            [sg.Multiline(size=(60,5), expand_x=True, expand_y=True, key='existedPaperName',enable_events=True)]
            ]
        
        #载入新文章的界面
        inputWindowLayout=[
            [sg.Text('文章载入系统，用于载入新的文章',font='Times 10')],
            [sg.Text('已载入文献数量{}'.format(self.numberPaperExisted),key="textOfPaperExisted",font='Times 15')],
            [sg.Button("选取文章")],
            [sg.Text('文章Id',font='Times 10',size=(8,1)),sg.Input(key='inputPaperId',size=(50,1))],
            [sg.Text('文章名称',font='Times 10',size=(8,1)),sg.Input(key='inputPaperName',size=(50,1),expand_x=True)],
            [sg.Text('文章语言',font='Times 10',size=(8,1)),sg.Combo(values=('中文', '英文'),default_value="中文",size=(10,1),readonly=True,key='inputPaperUsedLanguageMenu')],
            [sg.Button("载入文章")]
            ]
        
        #管理一个文章，详细修改信息的界面
        paperReadingLayout=[
            [sg.Button("选中文献"),sg.Button('确认修改')
             #,sg.Button('折叠界面'),sg.Button('专注模式')
             ],
            [sg.Listbox(values = self.existPaperNameList, 
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

        #将画面布局layout加入首上功能栏
        self.layout=[[sg.MenubarCustom(self.menuDef,key="MENU",font='Times 15',tearoff=True)],]
        #将画面布局layout加入全部界面栏
        self.layout+=[[sg.TabGroup([[sg.Tab("文献管理",manageWindowLayout)],
                               [sg.Tab("文献载入",inputWindowLayout)],
                               [sg.Tab("详细信息",paperReadingLayout)],
                               [sg.Tab('调试信息', logging_layout)]])        
            ]]
        #为画面布局layout设置窗口大小调整的小机关（右下角）
        self.layout[-1].append(sg.Sizegrip())
    #配置文件初始化
    def readConfigFile(self):
        #初始化配置文件管理对象，会直接尝试读取配置文件
        self.cFManager=paperAssistConfigManager(self.safeFolderPath,self.configFilePathName())
        #如果配置文件读取失败：
        if self.cFManager.flagPaperAssistFileInput==False:
            
            return 0
        #如果读取配置文件成功，在这里考虑都需要座什么操作    
    #定义一个新的后台文件管理对象
    def backendCreatNewProject(self,tempXmlFileName,tempFolderPath):
        return PaperDataXmlFileManagement(tempXmlFileName,tempFolderPath)
    #将前台数据保存到后台(同步功能，数据仍然在内存中)
    def savePaperData(self):
        try:
            #先判断一下是否已经定义了工程文件
            if self.currentBackendProject.xmlFilePath in("尚未定义工程.xml",""):
                sg.popup("尚未定义有工程文件",font='Times 15',keep_on_top=True)
                print("尚未定义有工程文件")
                return 0
            #保存一下文件
            for paperData in self.paperListFrontEnd:                
                self.currentBackendProject.inputPaperData(paperData)    
            return 1
        except Exception as err:
            print("[savePaperData]err:",err)
            #sg.popup("错误信息："+err,font='Times 15',keep_on_top=True)
            sg.popup("尚未有工程文件被初始化",font='Times 15',keep_on_top=True)
            print("尚未有工程文件被初始化")
    def saveXmlFile(self):
        #首先保存文件
        if not self.savePaperData() ==1 :
            print("[saveXmlFile]err:数据保存失败，无法保存文件")
            #数据保存失败，直接退出
            return 0        
        #数据保存成功，将文件导出来覆盖到原位
        self.currentBackendProject.saveXmlFile()
        print("导出了文件，名为",self.currentBackendProject.xmlFilePath,self.currentBackendProject.xmlFileName)
        
        return 1
    #新建一个后台管理对象，从xml文件中读取数据到后台，并保存到前台
    ##调用self.currentBackendProjectUpdate（）函数，输入新文件名，新文件所在文件夹路径，老文件的绝对路径下文件名
    def currentBackendProjectUpdate(self,newXmlFileName,newXmlFilePath,inputXmlFilePath):
        self.currentBackendProject=self.backendCreatNewProject(newXmlFileName,newXmlFilePath)
        print("选中了文件：{}，即将导入".format(inputXmlFilePath))
        self.currentBackendProject.readTreeFromXmlFile(inputXmlFilePath)
        print("成功导入文件{}，包含文章{}篇".format(newXmlFileName,len(self.currentBackendProject.paperDataList)))
        #把后台的paperDataList 传入到window用的paperList，并更新一些基本参数
        self.paperDataListUpdateBackeToFront()        
    #从后台把数据更新到前台
    def paperDataListUpdateBackeToFront(self):
        #将数据直接赋值更新
        self.paperListFrontEnd=self.currentBackendProject.paperDataList
        #更新numberPaperExisted数据
        self.numberPaperExisted=len(self.paperListFrontEnd)
        #更新numberPaperAvialable
        self.numberPaperAvialable=0
        for paper in self.paperListFrontEnd:
            print(paper.paperName)
            if paper.Availability==1:
                self.numberPaperAvialable+=1    
        self.windowNumberUpdate()
        
    #定义窗口部分变量更新的函数
    def windowNumberUpdate(self):
        self.window['textOfManagePaperNumber'].update('已载入文献数量{}，已读文献数量{}，可用文献数量{}'.
                                                      format(self.numberPaperExisted,self.numberPaperRead,self.numberPaperAvialable))
        self.window['textOfPaperExisted'].update('已载入文献数量{}'.format(self.numberPaperExisted))
        
        self.window['existedPaperName'].update(self.paperNameFormat())
        #window['existingPaperList'].TKListbox.delete(0, 'end')
        self.window['existingPaperList'].update(values=None)
        self.window['existingPaperList'].update(values=self.existPaperNameListUpdate())
        self.window['inputPaperId'].update(value="")
        self.window['inputPaperName'].update(value="")
    def existPaperNameListUpdate(self):
        existPaperNameList=[]
        for paper in self.paperListFrontEnd:
            existPaperNameList.append(str(paper.paperId)+" , "+paper.paperName)
        return existPaperNameList
    
    #定义函数，把所有文章的名字格式化出来
    def paperNameFormat(self):
        paperNameString=""
        for paper in self.paperListFrontEnd:
            paperNameString+=str(paper.paperId)+", "+paper.paperName+"\n"
        return paperNameString
    
    #针对"详细信息“界面下当前要处理的文章，将界面信息更新出来
    def windowCurrentPaperManagedInit(self):
        #这个文章对象初始化时id设为-1，如果此时<0，说明未被选中；注意，在使用完结后，也需要将其设为-1
        if self.currentPaperManaged.paperId<0:
            print("尚未选中要编辑的文章")
            return 0
        
        self.window['currentPaperId'].update(self.currentPaperManaged.paperId)
        self.window['currentPaperName'].update(self.currentPaperManaged.paperName)
        self.window['currentPaperUsedLanguage'].update(self.currentPaperManaged.languageList[self.currentPaperManaged.paperUsedLanguage])
        self.window['currentPaperPublicationLevel'].update(self.currentPaperManaged.publiocationList[self.currentPaperManaged.publicationLevel])
        self.window['currentPaperAvialablity'].update(self.currentPaperManaged.Availability)
        self.window['currentPaperFilePath'].update(self.currentPaperManaged.paperFilePath)
        self.window['currentPaperFiledLevel1'].update(self.currentPaperManaged.fieldLevel1)
        self.window['currentPaperFiledLevel2'].update(self.currentPaperManaged.fieldLevel2)
        self.window['currentPaperSummary'].update(self.currentPaperManaged.summaryReExtract)
        self.window['currentPapercharacteristic'].update(self.currentPaperManaged.characteristic)
        self.window['currentPapercompleteness'].update(self.currentPaperManaged.completeness)
    
    def windowCurrentPaperDataUpdate(self):
        tempName=self.window['currentPaperName'].get()
        tempLanguage=self.window['currentPaperUsedLanguage'].get()
        tempPublishedTime=self.window['currentPaperPublishTime'].get()
        tempPublishedLevel=self.window['currentPaperPublicationLevel'].get()
        #print(tempName,tempLanguage,tempPublishedTime,tempPublishedLevel)
        tempPaperAvialablity=self.window['currentPaperAvialablity'].get()
        tempPaperFieldLevel1=self.window['currentPaperFiledLevel1'].get()
        tempPaperFieldLevel2=self.window['currentPaperFiledLevel2'].get()
        tempPaperSummary=self.window['currentPaperSummary'].get()
        tempPapercharacteristic=self.window['currentPapercharacteristic'].get()
        self.currentPaperManaged.updatePaperName(tempName)
        self.currentPaperManaged.updatePaperUsedLanguage(tempLanguage)
        self.currentPaperManaged.updatePublishedTime(tempPublishedTime)
        self.currentPaperManaged.updatePublicationLevel(tempPublishedLevel)
        self.currentPaperManaged.updateAvialablity(str(tempPaperAvialablity))
        self.currentPaperManaged.updateFieldLevel1(tempPaperFieldLevel1)
        self.currentPaperManaged.updateFieldLevel2(tempPaperFieldLevel2)
        self.currentPaperManaged.updatePaperSummary(tempPaperSummary)
        self.currentPaperManaged.updatePapercharacteristic(tempPapercharacteristic)
        self.currentPaperManaged.paperDataOutput()
        for i in range(len(self.paperListFrontEnd)):
            if self.paperListFrontEnd[i].paperId==self.currentPaperManaged.paperId:
                self.paperListFrontEnd[i]=self.currentPaperManaged
                return 1
        print("[详细界面：异常]未找到相对应id的文章对象，当前编辑信息无法更新入前台文章列表")
        return 0
    #定义窗口事件相应函数
    def windowEventMainwindowEventMain(self):
        #定义窗口self.window
        self.window=sg.Window('阅读文献小助手(撰写综述中...)_V1.0',
                         self.layout,
                         right_click_menu=self.rightClickMenuDef,
                         right_click_menu_tearoff=True,
                         grab_anywhere=True,
                         resizable=True, 
                         margins=(0,0), 
                         use_custom_titlebar=True, 
                         finalize=True, 
                         keep_on_top=True,
                         return_keyboard_events=True)
        #设置窗口尺寸
        #self.window.set_min_size(self.window.size)
        #读取配置文件
        self.flagConfigFileRead=self.configFileManager.configFileInput()
        if not self.flagConfigFileRead==1:
            sg.popup_auto_close("配置文件读取失败，请手动添加一个工程",auto_close_duration=3,keep_on_top=True)
        else:
            tempString="上次登录时间"+self.configFileManager.lastLoginDate
            tempString+="\r\n上次退出时间"+self.configFileManager.lastLogoutDate
            tempString+="\r\n继续编辑工程"+self.configFileManager.lastUsingProjectFilePath
            
            sg.popup_auto_close(tempString,auto_close_duration=3,keep_on_top=True)
            inputXmlFilePath=self.configFileManager.lastUsingProjectFilePath
            tempOutputFilePathList=split(r'[/]',inputXmlFilePath)
            tempOutputFilePath=""
            if len(tempOutputFilePathList)>=1:  
                for i in range(0,len(tempOutputFilePathList)-1):
                    tempOutputFilePath+=tempOutputFilePathList[i]+"/"

            else:
                print("inputXmlFilePathList为空")
            tempXmlName=split(r'[/.]',inputXmlFilePath)[-2]
            print("tempXmlName=",tempXmlName)
            self.currentBackendProjectUpdate(tempXmlName, tempOutputFilePath, inputXmlFilePath)

        
        
        #while循环，接收并处理所有的窗口事件
        while True:
            event,values=self.window.read(timeout=100)
            #设置退出机制,退出while循环，直接结束全部流程
            if event in (None, sg.WIN_CLOSED,'关闭'):
                self.window.Close()
                break  
            #相应“创建工程”指令,需要输入xml文件的保存路径和文件名，并更新当前使用的后台文件管理对象
            ##创建工程的功能是主要功能之一，在配置文件导入失败或需要创建新工程时启用
            if event in ('创建工程'):
                 xmlFilePath = sg.popup_get_folder('选取保存路径', keep_on_top=True)
                 if xmlFilePath==None:
                     sg.popup("取消选择",font='Times 15',keep_on_top=True)
                     continue
                 #sg.popup("You chose: " + str(xmlFilePath), keep_on_top=True)
                 xmlFileName=sg.popup_get_text("输入工程名（无需后缀）",keep_on_top=True)
                 self.currentBackendProject=self.backendCreatNewProject(xmlFileName,xmlFilePath)
            #保存工程数据，
            if event in ('保存文件'):
                self.savePaperData()                 
            #将xml文件保存出来
            if event in ('导出文件'):
                #保存工程文件
                self.saveXmlFile()    
            #手动导入一个xml文件，用于初始化            
            ##的功能是主要功能之一，在配置文件导入失败或需要使用现有文件继续编辑的时候使用
            if event in ('导入文件'):
                #选取待读入的xml文件
                inputXmlFilePath=sg.popup_get_file("选取数据库XML文件",keep_on_top=True)
                #终止操作的对应处理
                if inputXmlFilePath==None:
                    sg.popup("取消选择",font='Times 15',keep_on_top=True)
                    continue
                #判断读入的xml文件名是否合法（后缀是不是.xml），如果合法继续执行
                if inputXmlFilePath.endswith(".xml"):
                    #newXmlFilePath = sg.popup_get_folder('选取保存路径', keep_on_top=True,default_path='D:\Mirror\沉头孔测量方法与加工误差分析综述\综述撰写辅助脚本\\')
                    #处理引入xml文件的全局名，提取其存储位置，用于输出文件地址的默认值
                    print("inputXmlFilePath=",inputXmlFilePath)
                    #处理一下刚才读入的文件绝对路径，分成文件夹路径tempOutputFilePath
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
                    #处理读入的xml文件名，分割出纯粹的文件名称（不带后缀），作为新建xml文件的默认文件名
                    tempXmlName=split(r'[/.]',inputXmlFilePath)[-2]
                    print("tempXmlName=",tempXmlName)
                    #弹出窗口，获取新xml文件的文件名（不需要后缀）
                    newXmlFileName=sg.popup_get_text("输入工程名（无需后缀）",keep_on_top=True,default_text=tempXmlName)
                    #获取新文件名的操作终止时，对应处理
                    if newXmlFileName in (None,""):
                        print("未输入有效的文件名")
                        continue
                    #调用self.currentBackendProjectUpdate（）函数，输入新文件名，新文件所在文件夹路径，老文件的绝对路径下文件名
                    self.currentBackendProjectUpdate(newXmlFileName, newXmlFilePath, inputXmlFilePath)
                #如果后缀不是(.xml)，直接报错（可能性不大）
                else:
                    print("导入文件出错：文件后缀错误")
            #选取一篇新的文章，重新导入，此时id会+1    ，后续应连接“载入文章”操作    
            if event in ("选取文章"):
                print("点击按钮，选取文章")
                paperFilePath=sg.popup_get_file('选取文章', keep_on_top=True)
                #global numberPaperExisted     
    
                if paperFilePath==None:
                    sg.popup("取消选择",font='Times 15',keep_on_top=True)
                    continue                
                #定义一个临时文章对象，使用的id就是self.numberPaperExisted
                tempPaper=PaperDataClass(self.numberPaperExisted)
                #向文章对象定义论文路径
                tempPaper.setFilePath(paperFilePath)
                #将文章路径提取出来，找到文章名字
                tempPaperName=split(r'[/.]',paperFilePath)[-2]
                #在界面中打印出文章id、文章名字
                self.window['inputPaperId'].update(tempPaper.paperId)
                self.window['inputPaperName'].update(tempPaperName)
                #将这个临时文章对象加入到前台文章列表中
                self.paperListFrontEnd.append(tempPaper)
                #处理完事件后，等待“载入文章”事件
            #承接“选取文章”操作，将导入的文章存入前台文章列表
            if event in ("载入文章"):
                print("文章确认无误，开始载入")
                #从窗口读入当前的文章id
                tempPaperId=int(self.window['inputPaperId'].get())
                #文章id与当前总文章数不符，说明“选取文章”和“载入文章”之间，窗口上的id发生了变化，这个时候报错，停止录入文献，self.numberPaperExisted也不发生变化
                if not tempPaperId==self.numberPaperExisted:
                    print("录入文章id发生异常变动，停止录入")
                    #此时停止录入，删除前台列表中的最后一个元素
                    self.paperListFrontEnd.pop()
                    continue
                #从窗口读入文章的名字和使用语言，此处可能有更改
                tempPaperName=self.window['inputPaperName'].get()
                tempPaperLanguage=self.window['inputPaperUsedLanguageMenu'].get()
                if tempPaperName in ('',None):
                    sg.popup("文章名为空",font='Times 15',keep_on_top=True)
                    continue
                if tempPaperLanguage in ('',None):
                    sg.popup("所用语言尚未定义",font='Times 15',keep_on_top=True)
                    continue
                self.paperListFrontEnd[tempPaperId].updatePaperName(tempPaperName)
                self.paperListFrontEnd[tempPaperId].updatePaperUsedLanguage(tempPaperLanguage)
                self.paperListFrontEnd[tempPaperId].paperDataOutput()
                self.numberPaperExisted+=1
                self.windowNumberUpdate()

            #详细信息界面的相应功能
            ##选中要编辑的文章，同时将其放入self.currentPaperManaged中
            if event in ("选中文献"):
                paperNameString=self.window['existingPaperList'].get()
                if paperNameString==[]:
                    sg.popup("尚未选中文献",font='Times 15',keep_on_top=True)
                    continue
                print("选中文献：",paperNameString)
                tempPaperId=int(str.split(paperNameString[0],',')[0])
                self.currentPaperManaged=self.paperListFrontEnd[tempPaperId]
                self.windowCurrentPaperManagedInit()
                
            ##将“详细信息”界面中填入的信息，修改进前台文章列表中
            if event in ("确认修改"):
                #paperNameString=self.window['existingPaperList'].get()
                #tempPaperId=int(str.split(paperNameString[0],',')[0])
                #currentPaper=paperList[tempPaperId]
                self.windowCurrentPaperDataUpdate()
            
            ##测试“折叠界面功能，其实是使用set_size()函数，重塑窗口尺寸
            if event in ("折叠界面"):
                #foldSize=(10,5)
                #sg.set_options(debug_win_size=(10,5),window_location=(5,5))
                print("设定窗口大小和位置")
                #self.window.size(foldSize)
            
            
            ##在“详细界面”中，通过窗口上文件地址，打开源文件pdf或caj文件,
            if event in ("打开源文件"):
                #从窗口读取“文章id"
                #tempId=int(self.window['currentPaperId'].get())
                #从窗口读取Paper Path，用于打开文件
                tempPaperPath=self.window['currentPaperFilePath'].get()
                if tempPaperPath.endswith(".pdf"):
                     #paperList[tempId].paperFilePath=tempPaperPath
                     open_new(tempPaperPath)
                     #window["currentPaperFilePath"].update(tempPaperPath)
                elif tempPaperPath.endswith(".caj"):
                     open_new(tempPaperPath)
                    
                else :
                    tempPaperPath=sg.popup_get_file("重新定义文件路径",title="文件路径不存在",keep_on_top=True)
                    if tempPaperPath.endswith(".pdf") or tempPaperPath.endswith(".caj"):
                        self.currentPaperManaged.paperFilePath=tempPaperPath
                        #self.paperListFrontEnd[tempId].paperFilePath=tempPaperPath
                        open_new(tempPaperPath)
                        self.window["currentPaperFilePath"].update(tempPaperPath)
                    #重新定义文件路径异常结束的应对方法    
                    else: 
                        print("tempPaperPath=",tempPaperPath)
                        #sg.popup("取消：定义文件路径")
                        self.window["currentPaperFilePath"].update("")
                        continue
                
                print("打开源文件，路径为",)
                
            if event in (self.keyboardCallBackDict["leftCtrl"],self.keyboardCallBackDict["rightCtrl"]):
                print("按键触发CTRL")    
                self.keyboardSaveFlag=True
            if event in ('s'):
                if self.keyboardSaveFlag==True:
                    print("保存")
                    self.saveXmlFile()       
                else : self.keyboardSaveFlag=False
            if event in ("保存配置文件"):
                print("保存配置文件",self.currentBackendProject.xmlFilePath+self.currentBackendProject.xmlFileName)
                
                self.configFileManager.configFileCreate(self.currentBackendProject.xmlFilePath+self.currentBackendProject.xmlFileName)
        print("保存配置文件",self.currentBackendProject.xmlFilePath+self.currentBackendProject.xmlFileName)
        self.configFileManager.configFileCreate(self.currentBackendProject.xmlFilePath+self.currentBackendProject.xmlFileName)
                


if __name__ == '__main__':
    #软件实例化
    paperAssistant=PaperImportGui2()
    #窗口设置初始化
    paperAssistant.windowLayoutInit()
    #窗口实例化，显示并运行
    paperAssistant.windowEventMainwindowEventMain()
    



































    
        
