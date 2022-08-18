# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 20:37:58 2022

@author: MengFt
"""

import time

class PaperDataClass(object):
    def __init__(self,paperId=-1):
        if (paperId<0):
            self.paperId=paperId
            print("请使用正确id定义文章")
            self.__del__()
            return 
        #定义一个类变量默认值的字典，用于初始化
        self.defaultValueDict={"paperName":"",
                               "paperUsedLanguage":0,    
                               "paperFilePath":"未载入",
                               "paperPicturePath":[],
                               "paperPublishTime":"",
                               "publicationLevel":0,
                               "publicationName":"未定义",
                               "fieldLevel1":"未定义",
                               "fieldLevel2":"未定义",
                               "summaryReExtract":"未输入",
                               "characteristic":"未输入",
                               "Availability":0}
        self.paperId=paperId #id≥0
        self.paperName=self.defaultValueDict["paperName"]
        self.languageList=("未定义","中文","英文","日文","西班牙语")
        self.paperUsedLanguage=self.defaultValueDict["paperUsedLanguage"]
        self.paperFilePath=self.defaultValueDict["paperFilePath"]
        self.paperPicturePath=self.defaultValueDict["paperPicturePath"]
        self.paperImportTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( int(time.time())))
        self.paperPublishTime=self.defaultValueDict["paperPublishTime"]
        self.publiocationList=("未定义","顶刊","顶会","非顶刊SCI1区","SCI2区","SCI3-4区","EI","中文核心")
        self.publicationLevel=self.defaultValueDict["publicationLevel"]
        self.publicationName=self.defaultValueDict["publicationName"]
        self.fieldLevel1=self.defaultValueDict["fieldLevel1"]
        self.fieldLevel2=self.defaultValueDict["fieldLevel2"]
        self.summaryReExtract=self.defaultValueDict["summaryReExtract"]
        self.characteristic=self.defaultValueDict["characteristic"]
        self.Availability=self.defaultValueDict["Availability"] 
        self.completeness=0
    #设定路径的函数
    def setFilePath(self,path):
        if path=="":
            print("路径为空，无法输入")
            return 0
        self.paperFilePath=path
        return 1
    #设定文章名的函数
    def updatePaperName(self,name):
        if name=="":
            print("文章设定：传入值为空，无法设定")
            return 0
        self.paperName=name
        return 1
    #设定文章所用语言的函数
    def updatePaperUsedLanguage(self,languageKeyOrNum):
        if languageKeyOrNum=="":
            print("语言设定：传入值为空，无法设定")
            return 0
        if type(languageKeyOrNum)==int:
            self.paperUsedLanguage=languageKeyOrNum
        else:
            print("languageKeyOrNum=",languageKeyOrNum)
            i=0
            for j in self.languageList:
                if languageKeyOrNum==j:
                    self.paperUsedLanguage=i
                else : i+=1
            #print(self.languageList[languageKeyOrNum])
            #self.paperUsedLanguage=self.languageList[languageKeyOrNum]
        return 1
    def updatePublishedTime(self,publishTime):
        if publishTime=="":
            print("发表时间设定：传入值为空，无法设定")
            return 0
        self.paperPublishTime=publishTime
        return 1
    def updatePublicationLevel(self,publicationLevel):
        if publicationLevel=="":
            print("发表水平设定：传入值为空，无法设定")
            return 0
        if type(publicationLevel)==int:
            self.publicationLevel=publicationLevel
        else:
            print("publishedLevel=",publicationLevel)
            i=0
            for j in self.publiocationList:
                if publicationLevel==j:
                    self.publicationLevel=i
                else : i+=1
            return 1
    def updateAvialablity(self,paperAvialablity):
        if paperAvialablity=="":
            print("文章可用性设定：传入值为空，无法设定")
            return 0
        if type(paperAvialablity)==str:
            if (paperAvialablity=="可用"):
                self.Availability=1
            elif (paperAvialablity=="不可用"):
                self.Availability=-1
            else: 
                self.Availability=0
            
        else:
            self.Availability=paperAvialablity            
        return 1
    
    def updateFieldLevel1(self,fieldLevel1):
        if fieldLevel1=="":
            print("文章1级领域设定：传入值为空，无法设定")
            return 0
        self.fieldLevel1=fieldLevel1
        
    def updateFieldLevel2(self,fieldLevel2):
        if fieldLevel2=="":
            print("文章2级领域设定：传入值为空，无法设定")
            return 0
        self.fieldLevel2=fieldLevel2

    def updatePaperSummary(self,paperSummary):
        if paperSummary=="":
            print("文章概设输入：传入值为空，无法设定")
            return 0
        self.summaryReExtract=paperSummary

    def updatePapercharacteristic(self,Papercharacteristic):
        if Papercharacteristic=="":
            print("文章特点输入：传入值为空，无法设定")
            return 0
        self.characteristic=Papercharacteristic
        
    def setAllPaperParaInOne(self,paperParaDict):
        #这个函数，可以一次性设置（几乎）所有的类变量
        #用于从xml文件中导入大量的信息
        if  paperParaDict==None:
            paperParaDict=self.defaultValueDict
        self.paperName=paperParaDict["paperName"]
        self.paperUsedLanguage=paperParaDict["paperUsedLanguage"]
        self.paperFilePath=paperParaDict["paperFilePath"]
        self.paperPicturePath=paperParaDict["paperPicturePath"]
        self.paperImportTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime( int(time.time())))
        self.paperPublishTime=paperParaDict["paperPublishTime"]
        self.publicationLevel=paperParaDict["publicationLevel"]
        self.publicationName=paperParaDict["publicationName"]
        self.fieldLevel1=paperParaDict["fieldLevel1"]
        self.fieldLevel2=paperParaDict["fieldLevel2"]
        self.summaryReExtract=paperParaDict["summaryReExtract"]
        self.characteristic=paperParaDict["characteristic"]
        self.Availability=paperParaDict["Availability"] 
        
        return 1
        

    def paperDataOutput(self):
        print("选取文章信息如下:id为{}，文章名称为{}，语言为{}".format(self.paperId,self.paperName,self.languageList[self.paperUsedLanguage]))
        print("发表刊物：{};刊物水平为{}，发表时间：{}".format(self.publicationName,self.publiocationList[self.publicationLevel],self.paperPublishTime))
        print("文章研究领域，一级领域：{}".format(self.fieldLevel1))
        print("文章研究领域，二级领域：{}".format(self.fieldLevel2))
        print("文章主旨：{}".format(self.summaryReExtract))
        print("文章特点：{}".format(self.characteristic))
        if self.Availability==1:
            print("文章可用于综述撰写")
        elif self.Availability==-1:
            print("文章无法用于综述撰写")
        else : print("文章可用性未定义")
        print("源文件名：{}".format(self.paperFilePath))
        return 0

        

    
    def __del__(self):
        print("析构了一个paperDataClass对象,paperId=",self.paperId)
    #文章使用语言：0：未知；1，中文；2，英文；

if __name__ == '__main__':

    rightPaper=PaperDataClass(0)
    
    rightPaper.setFilePath("123.pdf")
    rightPaper.updatePaperName("沉头孔加工精度分析")
    
    rightPaper.updateAvialablity("可用")
    print("在主函数里：",rightPaper.Availability)
    rightPaper.Availability=1
    print("在主函数里：",rightPaper.Availability)
    rightPaper.paperDataOutput()
    
