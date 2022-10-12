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
import os
from GrubAndCutScreen import GrubAndCutScreen
from PIL import Image,ImageGrab
from transTool import transTool
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
        self.mainWindowIcon_32 = b'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'
        
        #4.多窗口结构的系统变量
        ##第一个子窗口是否被激活的标志位
        self.flagSubWindowOneActive=False
        ##第二个子窗口是否被激活的标志位
        self.flagSubWindowTwoActive=False

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
        #右键唤出列表
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
            [sg.Button("选中文献"),sg.Button('确认修改'),sg.Button('删除文献'),
             sg.Button("进入专注模式"),sg.Button("管理文献图片")
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
        #专注模式，仅保留文献内容输入功能
        focusedReadingModeLayout=[
            [sg.Button("确认内容修改"),sg.Button("打开源文件_2"),sg.Button("谷歌翻译")],
            [sg.Text('文章主要内容',font='Times 10',size=(8,2)),
             sg.Multiline(size=(100,3), expand_x=True, expand_y=True, key='currentPaperSummary_2',enable_events=True)], #文章主要内容
            [sg.Text('特点或不足',font='Times 10',size=(8,2)),
             sg.Multiline(size=(100,3), expand_x=True, expand_y=True, key='currentPapercharacteristic_2',enable_events=True)],#文章特点
            ]

        #用于打印调试信息的界面
        logging_layout = [[sg.Button("调试功能1"),sg.Button("调试功能2")],
            [sg.Text("Anything printed will display here!",font='Times 10')],
                          [sg.Multiline(size=(60,15), font='Times 8', expand_x=True, expand_y=True, write_only=True,
                                        reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True, auto_refresh=True)]
                          ]

        #将画面布局layout加入首上功能栏
        self.layout=[[sg.MenubarCustom(self.menuDef,key="MENU",font='Times 15',tearoff=True)],]
        #将画面布局layout加入全部界面栏
        self.layout+=[[sg.TabGroup([[sg.Tab("文献管理",manageWindowLayout)],
                               [sg.Tab("文献载入",inputWindowLayout)],
                               [sg.Tab("详细信息",paperReadingLayout)],
                               [sg.Tab("专注模式",focusedReadingModeLayout)],
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
        if self.currentPaperManaged.paperId<0:
            print("尚未选中要编辑的文章")
            return 0
        
        self.window['currentPaperId'].update(self.currentPaperManaged.paperId)
        self.window['currentPaperName'].update(self.currentPaperManaged.paperName)
        self.window['currentPaperUsedLanguage'].update(self.currentPaperManaged.languageList[self.currentPaperManaged.paperUsedLanguage])
        if self.currentPaperManaged.paperPublishTime in (None,""):
            self.window['currentPaperPublishTime'].update("未输入")
        else:
            self.window['currentPaperPublishTime'].update(self.currentPaperManaged.paperPublishTime)
        self.window['currentPaperPublicationLevel'].update(self.currentPaperManaged.publiocationList[self.currentPaperManaged.publicationLevel])
        self.window['currentPaperAvialablity'].update(self.currentPaperManaged.Availability)
        self.window['currentPaperFilePath'].update(self.currentPaperManaged.paperFilePath)
        self.window['currentPaperFiledLevel1'].update(self.currentPaperManaged.fieldLevel1)
        self.window['currentPaperFiledLevel2'].update(self.currentPaperManaged.fieldLevel2)
        self.window['currentPaperSummary'].update(self.currentPaperManaged.summaryReExtract)
        self.window['currentPapercharacteristic'].update(self.currentPaperManaged.characteristic)
        self.window['currentPaperSummary_2'].update(self.currentPaperManaged.summaryReExtract)
        self.window['currentPapercharacteristic_2'].update(self.currentPaperManaged.characteristic)
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
    #删除一个文章的函数
    def deletePaperById(self,paperId):
        if paperId < 0 or paperId >= self.numberPaperExisted:
            print("删除文章流程异常：文章id不存在")
            return -1
        #删除前台的paperList
        self.paperListFrontEnd.pop(paperId)
        #删除后台的paperList,否则，删除将失效
        #self.paperListBackEnd.pop(paperId)
        #赶紧把当前前台文献数量减1
        self.numberPaperExisted-=1
        #判断一下，如果当前删除的是最后一位，就完事儿了；否则还得重新调整其他文章对象的id
        if not self.numberPaperExisted == paperId:
            for i in range(paperId,self.numberPaperExisted):
                self.paperListFrontEnd[i].paperId -=1
                #self.paperListBackEnd[i].paperId -=1
        return 1

    #返回当前时间
    def currentTime(self):
        currentTime=time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime( int(time.time())))
        return currentTime
#%%创建一个子窗口subWindow1所需要的全部函数都在这里：
    #子窗口1的逻辑循环
    def createSubWindowOneFromMain(self):
        #进入这个函数是为了激活子窗口1
        #先判断是否有选中的文章，如果否则return
        if self.currentPaperManaged.paperId<0:
            print("尚未选中要编辑的文章")
            sg.popup_auto_close("尚未选中要阅读的文章",auto_close_duration=1,keep_on_top=True)
            return 0
        

        if self.flagSubWindowOneActive==True:
            #重复打开子窗口1，应该是需要重新加载，此时应该针对性的处理
            #首先把 现在的窗口关掉，重新载入layout，重新加载subWindowOne
            self.subWindowOne.close()
            
            #return 0
        #在这儿判断是否已经选取了阅读文献
        else:
            #将标志位置位
            self.flagSubWindowOneActive=True
            #将主窗口隐藏
            self.window.Hide()
            #定义当前子窗口的函数
            subLayout=[
                [sg.Button("打开源文件",key="打开源文件_专注模式子界面"),sg.Button("百度翻译",key="BDtranslate"),sg.Button("清空翻译",key="clearTranslation"),sg.Button("翻译网站",key="BDTranslateInSubWindowOne"),sg.Button("确认内容修改"),],
                [sg.Text('文章主要内容',font='Times 10',size=(45,1)),sg.Text('翻译原文',font='Times 10',size=(10,1)),],
                [sg.Multiline(size=(20,30),font='Times 16', expand_x=True, expand_y=True,key="summaryInSubWindowOne",enable_events=True),
                 sg.Multiline(size=(20,30),font='Times 12', expand_x=True, expand_y=True,key="textBeforeTranslate",enable_events=True)], #文章主要内容
                [sg.Text('特点或不足',font='Times 10',size=(45,1)),sg.Text('翻译译文',font='Times 10',size=(10,1)),],
                [sg.Multiline(size=(20,30),font='Times 16', expand_x=True, expand_y=True,key="charaInSubWindowOne",enable_events=True),
                 sg.Multiline(size=(20,30),font='Times 12', expand_x=True, expand_y=True,key="textAfterTranslate",enable_events=True)],#文章特点  
                ]
        #为画面布局layout设置窗口大小调整的小机关（右下角）
        subLayout[-1].append(sg.Sizegrip())
        
        windowSize=self.getScreenSize()
        subWindowOneSize=(500,windowSize[1]-80)
        subWindowOneLocation=(windowSize[0]-subWindowOneSize[0]-60,0)        
        print("当前屏幕尺寸：{}；子窗口尺寸：{}；子窗口位置：{}".format(windowSize,subWindowOneSize,subWindowOneLocation))
        #创建窗口函数
        self.subWindowOne=sg.Window("专注阅读，心无杂念！",
                                    subLayout,
                                    resizable=True, 
                                    grab_anywhere=True,
                                    keep_on_top=True,
                                    finalize=True, 
                                    location=(subWindowOneLocation),
                                    )
        
        self.subWindowOne.set_min_size(subWindowOneSize)
        self.subWindowOne["summaryInSubWindowOne"].update(self.currentPaperManaged.summaryReExtract)
        self.subWindowOne["charaInSubWindowOne"].update(self.currentPaperManaged.characteristic)
        #初始化翻译工具
        BDTransTool=transTool()
        
        while True:
            sub1Event,sub1Values=self.subWindowOne.read(timeout=1000)       
            if not sub1Event in (None,"__TIMEOUT__"):    
                print("当前时间为：{}，子窗口1激活事件{}".format(self.currentTime(),sub1Event))
            #定时保存，如果长达1s钟没有新动作，就直接保存
            if sub1Event in ("__TIMEOUT__",):
                self.saveChangeInSubWindowOne()
                #print("当前时间为：{}，子窗口1激活事件{}".format(self.currentTime(),sub1Event))
            #如果关闭子窗口，自动重新打开主窗口                
            if sub1Event in (sg.WIN_CLOSED,'关闭'):
                self.subWindowOne.close()
                self.flagSubWindowOneActive=False
                self.window.UnHide()
                break
            if sub1Event in ("确认内容修改"):
                #将“专注模式”下输入的文章主要内容，更新到前台系统数据中，并刷新“详细信息”中的相应内容
                self.saveChangeInSubWindowOne()
            if sub1Event in("打开源文件_专注模式子界面"):
                #从窗口读取“文章id"
                #tempId=int(self.window['currentPaperId'].get())
                #从窗口读取Paper Path，用于打开文件
                try:
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
                except Exception as err:
                    print("打开源文件流程报错：",err)
            if sub1Event in ("GGTranslateInSubWindowOne"):
                #打开谷歌翻译，直接设置为英文翻中文模式
                open_new("https://translate.google.cn/?sl=en&tl=zh-CN&op=translate")
                print("打开网址：https://translate.google.cn/")
            if sub1Event in ("BDTranslateInSubWindowOne"):
                #打开百度翻译，直接设置为英文翻中文模式
                open_new("https://fanyi.baidu.com/#en/zh")
                print("打开网址：https://fanyi.baidu.com/#en/zh")
            
            if sub1Event in ("BDtranslate"):
                stringBeforeTrans=self.subWindowOne["textBeforeTranslate"].get()
                #框里没有内容，不翻译了
                if stringBeforeTrans in ("",None):
                    print("没有东西，不翻译了")
                    continue
                BDTransTool.inputString(stringBeforeTrans,transType=0,deleteWrap=True)
                stringAfterTrans=BDTransTool.getTrans()
                print("翻译后：",stringAfterTrans)
                stringBeforeTrans=BDTransTool.inputWords
                self.subWindowOne["textBeforeTranslate"].update(stringBeforeTrans)
                self.subWindowOne["textAfterTranslate"].update(stringAfterTrans)
            
            if sub1Event in ("clearTranslation"):
                self.subWindowOne["textBeforeTranslate"].update("")
                self.subWindowOne["textAfterTranslate"].update("")
                    
        return 1
    
    
    
    #读取屏幕尺寸
    def getScreenSize(self):
        image = ImageGrab.grab()

        height=image.height
        width=image.width
        return (width,height)



    def saveChangeInSubWindowOne(self):
        #将“专注模式”下输入的文章主要内容，更新到前台系统数据中，并刷新“详细信息”中的相应内容
        tempPaperSummary=self.subWindowOne['summaryInSubWindowOne'].get()
        self.currentPaperManaged.updatePaperSummary(tempPaperSummary)
        self.window['currentPaperSummary'].update(tempPaperSummary)
        self.window['currentPaperSummary_2'].update(tempPaperSummary)
        #将“专注模式”下输入的文章特点，更新到前台系统数据中，并刷新“详细信息”中的相应内容
        tempPapercharacteristic=self.subWindowOne['charaInSubWindowOne'].get()
        self.currentPaperManaged.updatePapercharacteristic(tempPapercharacteristic)
        self.window['currentPapercharacteristic'].update(tempPapercharacteristic)
        self.window['currentPapercharacteristic_2'].update(tempPapercharacteristic)
        #根据文章id查询，完成前台到后台的刷新，保证前后台数据一致
        for i in range(len(self.paperListFrontEnd)):
            if self.paperListFrontEnd[i].paperId==self.currentPaperManaged.paperId:
                self.paperListFrontEnd[i]=self.currentPaperManaged
                continue


#%%创建一个子窗口subWindow2所需要的全部函数，用于加载和管理图片
    #子窗口2的逻辑循环
    def createSubWindowTwoFromMain(self):
        #进入这个函数是为了激活子窗口2
        #先判断是否有选中的文章，如果否则return
        if self.currentPaperManaged.paperId<0:
            print("尚未选中要编辑的文章")
            sg.popup_auto_close("尚未选中要阅读的文章",auto_close_duration=1,keep_on_top=True)
            return 0
        #如果当前flagSubWindowTwoActive为true说明是重新
        if self.flagSubWindowTwoActive==True:
            self.subWindowTwo.close()
        else:
            self.flagSubWindowTwoActive=True
            self.window.hide()
            #这里应该把图片预加载进去
        imageSize=(640,480)
        subWindowTwoSize=(imageSize[0]+30,imageSize[1]*2+50)
        #subWindowTwoSize=(imageSize[0]*2,imageSize[1])

        try:
            img1FileName=self.currentPaperManaged.paperPicturePathList[0]
            if not img1FileName.endswith("png"):
                img1FileName=".\imageLibrary\imgSample1.png"
                
        except Exception as e:  
            img1FileName=".\imageLibrary\imgSample.png"
            print("图片1导入错误,",e)
        try:
            img2FileName=self.currentPaperManaged.paperPicturePathList[1]
            if not img2FileName.endswith("png"):
                img2FileName=".\imageLibrary\imgSample2.png"
                
        except Exception as e:  
            img2FileName=".\imageLibrary\imgSample2.png"
            print("图片1导入错误,",e)
        tempSize1=self.pictureResize(img1FileName,img1FileName,size=imageSize,reShape=False,type="png")
        tempSize2=self.pictureResize(img2FileName,img2FileName,size=imageSize,reShape=False,type="png")
        if (not tempSize1==-1) and (not tempSize2==-1):
            subWindowTwoSize=(max(tempSize1[0],tempSize2[0])+30,tempSize1[1]+tempSize2[1]+50)
        else:
            tempSize1=imageSize
            tempSize2=imageSize
            
        #控制一下最多的图片,在这儿强制图片最大数量是4张
        self.currentPaperManaged.maxPictureNumber=4
        self.currentPaperManaged.controlPictureNumber()
        print("666666")
        print("当前文章图片地址为：",self.currentPaperManaged.paperPicturePathList)
        subLayout=[
            [sg.Button("载入图片1"),sg.Button("删除图片1"),sg.Button("载入图片2"),sg.Button("删除图片2"),sg.Button("刷新子窗口"),sg.Button("打开源文件",key="打开源文件_图片管理界面")],
            [sg.Image(filename=img1FileName,key="sub2Image1",size=tempSize1),],
            [sg.Image(filename=img2FileName,key="sub2Image2",size=tempSize2)],
            ]
            
        subLayout[-1].append(sg.Sizegrip())
        
        windowSize=self.getScreenSize()
        subWindowTLocation=(windowSize[0]-subWindowTwoSize[0]-20,0)        
        print("当前屏幕尺寸：{}；子窗口尺寸：{}；子窗口位置：{}".format(windowSize,subWindowTwoSize,subWindowTLocation))

        self.subWindowTwo=sg.Window("图片管理",
                                    subLayout,
                                    resizable=True, 
                                    grab_anywhere=True,
                                    keep_on_top=True,
                                    finalize=True, 
                                    location=subWindowTLocation,)
        self.subWindowTwo.set_min_size(subWindowTwoSize)
        while True:
            sub2Event,sub2Values=self.subWindowTwo.read(timeout=100)      
            if sub2Event in (None, sg.WIN_CLOSED,'关闭'):
                self.subWindowTwo.close()
                self.flagSubWindowTwoActive=False
                self.window.UnHide()
                break
            if sub2Event in("打开源文件_图片管理界面"):
                #从窗口读取“文章id"
                #tempId=int(self.window['currentPaperId'].get())
                #从窗口读取Paper Path，用于打开文件
                try:
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
                except Exception as err:
                    print("打开源文件流程报错：",err)

            if sub2Event in ("刷新子窗口"):
                #self.refreshSubWindowTwo()
                self.createSubWindowTwoFromMain()
            if sub2Event in ("载入图片1") :
                img1Path=sg.popup_get_folder("选取存储地址", keep_on_top=True,default_path="./imageLibrary")
                img1Path+="/"
                img1Name="PaperId_"+str(self.currentPaperManaged.paperId)+"_img1.png"
                img1Path+=img1Name
                print("img1Path=",img1Path)
                self.subWindowTwo.Hide()
                cutScreen=GrubAndCutScreen(img1Path)
                cutScreen.imageCutWithMouse()
                
                if len(self.currentPaperManaged.paperPicturePathList)>0:
                    self.currentPaperManaged.paperPicturePathList[0]=img1Path
                else:
                    print("333333:",self.currentPaperManaged.paperPicturePathList)

                    self.currentPaperManaged.paperPicturePathList.append(img1Path)
                    print("444444:",self.currentPaperManaged.paperPicturePathList)
                self.subWindowTwo.UnHide()
                self.createSubWindowTwoFromMain()
            if sub2Event in ("删除图片1"):
                if len(self.currentPaperManaged.paperPicturePathList)>0:
                    img1FileName=self.currentPaperManaged.paperPicturePathList[0]
                    if img1FileName.endswith("png"):
                        try:
                            os.remove(img1FileName)
                        except Exception as e:
                            print ("图片1删除流程异常:",e)
                    self.currentPaperManaged.paperPicturePathList[0]=""
                
                self.createSubWindowTwoFromMain()
            if sub2Event in ("载入图片2") :
                img2Path=sg.popup_get_folder("选取存储地址", keep_on_top=True,default_path=".\imageLibrary\\")
                img2Name="PaperId_"+str(self.currentPaperManaged.paperId)+"_img2.png"
                img2Path+=img2Name
                print("img2Path=",img2Path)
                self.subWindowTwo.Hide()
                cutScreen=GrubAndCutScreen(img2Path)
                cutScreen.imageCutWithMouse()
                
                if len(self.currentPaperManaged.paperPicturePathList)<1:
                    self.currentPaperManaged.paperPicturePathList=[]
                    self.currentPaperManaged.paperPicturePathList.append("")
                    self.currentPaperManaged.paperPicturePathList.append(img2Path)
                elif len(self.currentPaperManaged.paperPicturePathList)==1:
                    self.currentPaperManaged.paperPicturePathList.append(img2Path)
                else:
                    self.currentPaperManaged.paperPicturePathList[1]=img2Path
                print("555555:")
                print("当前文章图片地址为：",self.currentPaperManaged.paperPicturePathList)
                self.subWindowTwo.UnHide()
                self.createSubWindowTwoFromMain()
            if sub2Event in ("删除图片2"):
                if len(self.currentPaperManaged.paperPicturePathList)>1:
                    img2FileName=self.currentPaperManaged.paperPicturePathList[1]
                    if img2FileName.endswith("png"):
                        try:
                            os.remove(img2FileName)
                        except Exception as e:
                            print ("图片2删除流程异常:",e)
                    self.currentPaperManaged.paperPicturePathList[1]=""
                
    #刷新子窗口2，如果有新的图片，要抓紧显示出来   
    def refreshSubWindowTwo(self):
        #关闭，但是不清空标志位
        self.subWindowTwo.close()
        self.createSubWindowTwoFromMain()
        #图片尺寸重置
        
    def pictureResize(self,inputPath,outputPath,size=(600,600),reShape=False,type="png"):
        try:
            inputImage=Image.open(inputPath)
            #不改变外形，以高度为准
            if reShape==False:
                height=int(size[1])
                width=int(inputImage.size[0]/inputImage.size[1]*size[1])
            #改变外形，长宽都完全按照要求
            else:
                height=int(size[1])
                width=int(size[0])
            outputImage = inputImage.resize((width,height),Image.ANTIALIAS)                    
            outputImage.save(outputPath,type)
            print("图片原尺寸为：",inputImage.size)
            print("图片{}更新完成，尺寸为{}×{}".format(inputPath,width,height))
            return [width,height]
        except Exception as e:
            print("图片尺寸更新失败",e)
            return -1
        
#%%定义主窗口事件和逻辑

    def windowEventMainwindowEventMain(self):
        #定义窗口self.window
        self.window=sg.Window('阅读文献小助手(撰写综述中...)_V1.0',
                         self.layout,
                         right_click_menu=self.rightClickMenuDef,
                         right_click_menu_tearoff=True,
                         grab_anywhere=True,
                         resizable=True, 
                         margins=(0,0), 
                         #use_custom_titlebar=True, 
                         finalize=True, 
                         keep_on_top=True,
                         #return_keyboard_events=True,
                         titlebar_background_color=sg.GREENS[3],
                         use_custom_titlebar=True, 
                         titlebar_icon=self.mainWindowIcon_32,
                         titlebar_font=(sg.DEFAULT_FONT, 14, 'bold'), 
                         icon=self.mainWindowIcon_32
                         )
        #设置窗口尺寸
        #self.window.set_min_size(self.window.size)
        self.window.set_min_size((820,270))
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
            if not event in ("__TIMEOUT__"):    
                print("当前时间为：{}，激活事件{}".format(self.currentTime(),event))
            if event in ('调试功能1'):
                print("执行调试功能1：")
                ########
                #self.window.close()
                ##########
                continue
            if event in ('调试功能2'):
                print("执行调试功能2：")
                #####################
                try:
                    print(self.window.size)
                    
                except Exception as err:
                    print(err)
                ######################
                continue
            
            
            
            #相应“创建工程”指令,需要输入xml文件的保存路径和文件名，并更新当前使用的后台文件管理对象
            ##创建工程的功能是主要功能之一，在配置文件导入失败或需要创建新工程时启用
            if event in ('创建工程'):
                 xmlFilePath = sg.popup_get_folder('选取保存路径', keep_on_top=True)
                 if xmlFilePath==None:
                     sg.popup("取消选择",font='Times 15',keep_on_top=True)
                     continue
                 #sg.popup("You chose: " + str(xmlFilePath), keep_on_top=True
                 #文件路径需要加一个“/”
                 xmlFilePath+="/"
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
            if event in ("删除文献"):
                #删除一篇文献
                #删除的是
                paperNameString=self.window['existingPaperList'].get()
                if (sg.popup_ok_cancel("是否删除当前文章：{}".format(paperNameString),font='Times 15',keep_on_top=True))=='OK':                
                    if paperNameString==[]:
                        sg.popup("尚未选中待删除文献",font='Times 15',keep_on_top=True)
                        continue
                    print("删除文献：",paperNameString)
                    tempPaperId=int(str.split(paperNameString[0],',')[0])
                    #删除id对应的文章，同时重整文章id
                    self.deletePaperById(tempPaperId)
                    self.windowNumberUpdate()
                else:
                    print("删除流程取消")
                    

                
            if event in ("确认内容修改"):
                #将“专注模式”下输入的文章主要内容，更新到前台系统数据中，并刷新“详细信息”中的相应内容
                tempPaperSummary=self.window['currentPaperSummary_2'].get()
                self.currentPaperManaged.updatePaperSummary(tempPaperSummary)
                self.window['currentPaperSummary'].update(tempPaperSummary)
                #将“专注模式”下输入的文章特点，更新到前台系统数据中，并刷新“详细信息”中的相应内容
                tempPapercharacteristic=self.window['currentPapercharacteristic_2'].get()
                self.currentPaperManaged.updatePapercharacteristic(tempPapercharacteristic)
                self.window['currentPapercharacteristic'].update(tempPapercharacteristic)
                #根据文章id查询，完成前台到后台的刷新，保证前后台数据一致
                for i in range(len(self.paperListFrontEnd)):
                    if self.paperListFrontEnd[i].paperId==self.currentPaperManaged.paperId:
                        self.paperListFrontEnd[i]=self.currentPaperManaged
                        continue
                
            
            
            ##在“详细界面”中，通过窗口上文件地址，打开源文件pdf或caj文件,
            if event in ("打开源文件","打开源文件_2"):
                #从窗口读取“文章id"
                #tempId=int(self.window['currentPaperId'].get())
                #从窗口读取Paper Path，用于打开文件
                try:
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
                except Exception as err:
                    print("打开源文件流程报错：",err)
              
            if event in ("谷歌翻译"):
                #打开谷歌翻译，直接设置为英文翻中文模式
                open_new("https://translate.google.cn/?sl=en&tl=zh-CN&op=translate")
                print("打开网址：https://translate.google.cn/")
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
        
            if event in ("进入专注模式"):
                try:
                    self.createSubWindowOneFromMain()
                except Exception as e:
                    print(e)
                
            if event in ("管理文献图片"):
                try:
                    self.createSubWindowTwoFromMain()
                except Exception as e:
                    print (e)
        
        #在结束流程前，保存一下工程文件
        self.saveXmlFile()
        print("保存配置文件",self.currentBackendProject.xmlFilePath+self.currentBackendProject.xmlFileName)
        
        self.configFileManager.configFileCreate(self.currentBackendProject.xmlFilePath+self.currentBackendProject.xmlFileName)
                


if __name__ == '__main__':
    #软件实例化
    paperAssistant=PaperImportGui2()
    #窗口设置初始化
    paperAssistant.windowLayoutInit()
    #窗口实例化，显示并运行
    paperAssistant.windowEventMainwindowEventMain()
    



































    
        
