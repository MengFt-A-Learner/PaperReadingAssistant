# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 09:28:54 2022

@author: MengFt
"""

import xml.etree.ElementTree as ET
from PaperDataClass import PaperDataClass


class PaperDataXmlFileManagement(object):
    #在传入固定xml的根节点后，根据
    def __init__(self,rootName="凡通撰写个文献综述",xmlFilePath=''):
        #定义xml文件的根节点
        self.root=ET.Element(rootName)
        #定义文件保存地址
        self.xmlFilePath=xmlFilePath
        #定义文件名，与根节点一个名字
        self.xmlFileName=rootName+'.xml'
        #定义xml数据结构
        self.paperDataTree=ET.ElementTree(self.root)
        #xml文件中需要管理的文件数据列表
        self.paperDataList=[]
        self.paperChildRootList=[]
        self.paperIdRootList=[]
        self.paperNameRootList=[]
        self.paperLanguageRootList=[]
        self.paperFilePathRootList=[]
        self.paperPublishTimeRootList=[]
        self.publicationLevelRootList=[]
        self.AvailabilityRootList=[]
        self.completenessRootList=[]
        self.fieldLevel1RootList=[]
        self.fieldLevel2RootList=[]
        self.summaryReExtractRootList=[]
        self.characteristicRootList=[]
    #新建一个文章的子节点，需要传入节点的名字
    def creatPaperChildRoot(self,paperChildRootName,inputPaperData):
        #定义一个子节点
        if paperChildRootName in (None,""):
            paperChildRootName="paperId_Undefined"
        tempPaperRoot=ET.SubElement(self.root, paperChildRootName)
        #存入子节点列表中加以管理
        self.paperChildRootList.append(tempPaperRoot)       
        #定义文章子节点的孙节点。注：我儿宣池贼帅！
        tempIndex=len(self.paperChildRootList)-1
        #1.paperId
        self.paperIdRootList.append(ET.SubElement(tempPaperRoot, "paperId"))
        self.paperIdRootList[tempIndex].text=str(inputPaperData.paperId)
        #2.paperName
        self.paperNameRootList.append(ET.SubElement(tempPaperRoot, "paperName"))
        self.paperNameRootList[tempIndex].text=inputPaperData.paperName
        #3.paperUsedLanguage
        self.paperLanguageRootList.append(ET.SubElement(tempPaperRoot, "paperLanguage"))
        self.paperLanguageRootList[tempIndex].text=str(inputPaperData.paperUsedLanguage)
        #4.paperPicturePath
        self.paperFilePathRootList.append(ET.SubElement(tempPaperRoot, "paperFilePath"))
        self.paperFilePathRootList[tempIndex].text=inputPaperData.paperFilePath
        #5.paperPublishTime
        self.paperPublishTimeRootList.append(ET.SubElement(tempPaperRoot, "paperPublishTime"))
        self.paperPublishTimeRootList[tempIndex].text=inputPaperData.paperPublishTime
        #6.publicationLevel
        self.publicationLevelRootList.append(ET.SubElement(tempPaperRoot, "publicationLevel"))
        self.publicationLevelRootList[tempIndex].text=str(inputPaperData.publicationLevel)
        #7.Availability
        self.AvailabilityRootList.append(ET.SubElement(tempPaperRoot, "Availability"))
        self.AvailabilityRootList[tempIndex].text=str(inputPaperData.Availability)
        #8.completeness
        self.completenessRootList.append(ET.SubElement(tempPaperRoot, "completeness"))
        self.completenessRootList[tempIndex].text=str(inputPaperData.completeness)       
        #9.fieldLevel1
        self.fieldLevel1RootList.append(ET.SubElement(tempPaperRoot, "fieldLevel1"))
        self.fieldLevel1RootList[tempIndex].text=str(inputPaperData.fieldLevel1)
        #10.fieldLevel2
        self.fieldLevel2RootList.append(ET.SubElement(tempPaperRoot, "fieldLevel2"))
        self.fieldLevel2RootList[tempIndex].text=str(inputPaperData.fieldLevel2)        
        #11.summaryReExtract
        self.summaryReExtractRootList.append(ET.SubElement(tempPaperRoot, "summaryReExtract"))
        self.summaryReExtractRootList[tempIndex].text=str(inputPaperData.summaryReExtract)        
        #12.characteristic
        self.characteristicRootList.append(ET.SubElement(tempPaperRoot, "characteristic"))
        self.characteristicRootList[tempIndex].text=str(inputPaperData.characteristic)                



        
    def updateExistedPaperChildRoot(self,tempIndex,tempPaperRoot,inputPaperData):
        
        #定义文章子节点的孙节点。注：我儿宣池贼帅！
        #1.paperId
        self.paperIdRootList[tempIndex].text=str(inputPaperData.paperId)
        #2.paperName
        self.paperNameRootList[tempIndex].text=inputPaperData.paperName
        #3.paperUsedLanguage
        self.paperLanguageRootList[tempIndex].text=str(inputPaperData.paperUsedLanguage)
        #4.paperPicturePath
        self.paperFilePathRootList[tempIndex].text=inputPaperData.paperFilePath
        #5.paperPublishTime
        self.paperPublishTimeRootList[tempIndex].text=inputPaperData.paperPublishTime
        #6.publicationLevel
        self.publicationLevelRootList[tempIndex].text=str(inputPaperData.publicationLevel)
        #7.Availability
        self.AvailabilityRootList[tempIndex].text=str(inputPaperData.Availability)
        #8.completeness
        self.completenessRootList[tempIndex].text=str(inputPaperData.completeness)       
        #9.fieldLevel1
        self.fieldLevel1RootList[tempIndex].text=str(inputPaperData.fieldLevel1)
        #10.fieldLevel2
        self.fieldLevel2RootList[tempIndex].text=str(inputPaperData.fieldLevel2)        
        #11.summaryReExtract
        self.summaryReExtractRootList[tempIndex].text=str(inputPaperData.summaryReExtract)        
        #12.characteristic
        self.characteristicRootList[tempIndex].text=str(inputPaperData.characteristic)                
        #13.        
        #14.        
        #15.      
        #16.
        
        
        
        
        
        
        
    
    def inputPaperData(self,paperData):
        tempIndex=0
        paperExistedFlag=False
        #遍历当前xml文件内管理的文件，根据id判断是否已经存在
        #如果存在，则直接将已有的paperData对象覆盖更新
        for tempIndex in range(0,len(self.paperDataList)):
            if paperData.paperId==self.paperDataList[tempIndex].paperId:
                self.paperDataList[tempIndex]=paperData
                paperExistedFlag=True
                break
        #如果遍历后发现不存在，则新增一个对象
        if paperExistedFlag==False:
            #先准备好这个对象在数组内的索引
            tempIndex=len(self.paperDataList)
            #新增这个对象
            self.paperDataList.append(paperData)
            #新增这个文章的节点
            tempPaperRootName="paperId"+str(paperData.paperId)
            #tempPaperRootName="paper"
            self.creatPaperChildRoot(tempPaperRootName,self.paperDataList[tempIndex])
            return 1
        #将新增的这个对象，每个值都存入到xml结构对象的相应节点中
        print("tempIndex=",tempIndex)
        print("len(self.paperChildRootList)",len(self.paperChildRootList))
        print("len(self.paperDataList)",len(self.paperDataList))
        if len(self.paperChildRootList)==len(self.paperDataList):            
            self.updateExistedPaperChildRoot(tempIndex,self.paperChildRootList[tempIndex],self.paperDataList[tempIndex])
        #出现了意想不到的bug，在进入函数之前，不知为何，paperDataList比paperChildRootList多1，导致不会正常进入内容和节点更新分支
        elif len(self.paperChildRootList)<len(self.paperDataList):
            tempPaperData=self.paperDataList[-1]
            tempPaperRootName="paperId"+str(tempPaperData.paperId)
            self.creatPaperChildRoot(tempPaperRootName,tempPaperData)
        else : 
            print("xml节点更新错误：节点数量多于内容数量！！")
            return 0 
        return 2

    def saveXmlFile(self,fileName=''):
        if fileName=="":
            fileName=self.xmlFilePath+'\\'+self.xmlFileName
        #self.paperDataTree=ET.ElementTree(self.root)
        self.paperDataTree.write(fileName,encoding='UTF-8')
        
    def readTreeFromXmlFile(self,filePath):
        if filePath in (None,''):
            print("从XML文件中读取数据出错：路径为",filePath)
            return 0
        try:
            self.paperDataTree=ET.parse(filePath)
        except:
            print("读取XML文件失败")
            return 0
        #成功读取xml树状结构
        print("成功读入文件{}，正在分析".format(filePath))
        #1.读取根节点
        self.root=self.paperDataTree.getroot()
        #2.读取文章子节点
        self.paperDataList=[]
        

        for paperData in self.root:
            #把每一个文章节点存入paperChildRootList，在更新和管理的时候有用
            self.paperChildRootList.append(paperData)  
            
            tempPaperIdRoot=paperData.find("paperId")
            self.paperIdRootList.append(tempPaperIdRoot)
            
            tempPaperNameRoot=paperData.find("paperName")
            self.paperNameRootList.append(tempPaperNameRoot)
            
            tempPaperLanguageRoot=paperData.find("paperLanguage")
            self.paperLanguageRootList.append(tempPaperLanguageRoot)

            tempPaperFilePathRoot=paperData.find("paperFilePath")
            self.paperFilePathRootList.append(tempPaperFilePathRoot)

            tempPaperPublishTimeRoot=paperData.find("paperPublishTime")
            self.paperPublishTimeRootList.append(tempPaperPublishTimeRoot)

            tempPublicationLevelRoot=paperData.find("publicationLevel")
            self.publicationLevelRootList.append(tempPublicationLevelRoot)

            tempAvailabilityRoot=paperData.find("Availability")
            self.AvailabilityRootList.append(tempAvailabilityRoot)

            tempCompletenessRoot=paperData.find("completeness")
            self.completenessRootList.append(tempCompletenessRoot)

            tempFieldLevel1Root=paperData.find("fieldLevel1")
            self.fieldLevel1RootList.append(tempFieldLevel1Root)
            
            tempFieldLevel2Root=paperData.find("fieldLevel2")
            self.fieldLevel2RootList.append(tempFieldLevel2Root)
            
            tempSummaryReExtractRoot=paperData.find("summaryReExtract")
            self.summaryReExtractRootList.append(tempSummaryReExtractRoot)
            
            tempCharacteristicRoot=paperData.find("characteristic")
            self.characteristicRootList.append(tempCharacteristicRoot)
            #新建一个paperData的类，用于存储这些数据，并存入paperDataList中
            
            tempPaperData=PaperDataClass(int(tempPaperIdRoot.text))
            print("导入一个文件对象，id为",tempPaperIdRoot.text)
            #将文章的数据保存成dict型，用于设定paperData类对象
            tempPaperDataDict={"paperName":tempPaperNameRoot.text,
                                   "paperUsedLanguage":int(tempPaperLanguageRoot.text),    
                                   "paperFilePath":tempPaperFilePathRoot.text,
                                   "paperPicturePath":[],
                                   "paperPublishTime":tempPaperPublishTimeRoot.text,
                                   "publicationLevel":int(tempPublicationLevelRoot.text),
                                   "publicationName":"未定义",
                                   "fieldLevel1":tempFieldLevel1Root.text,
                                   "fieldLevel2":tempFieldLevel2Root.text,
                                   "summaryReExtract":tempSummaryReExtractRoot.text,
                                   "characteristic":tempCharacteristicRoot.text,
                                   "Availability":int(tempAvailabilityRoot.text)}
            #查看paperDataClass获取相应设定
            tempPaperData.setAllPaperParaInOne(tempPaperDataDict)
            self.paperDataList.append(tempPaperData)
            
        return 1
            
            
            
            


"""        
xmlFileTest1=PaperDataXmlFileManagement("xmlFileTest")
Paper0=PaperDataClass(0)
Paper0.setFilePath("123.pdf")
Paper0.updatePaperName("沉头孔加工精度分析")
Paper0.updatePaperUsedLanguage(1)
Paper0.paperDataOutput()

xmlFileTest1.inputPaperData(Paper0)


Paper0.paperPublishTime="2020-07-08"
xmlFileTest1.inputPaperData(Paper0)
       
Paper1=PaperDataClass(1)
Paper1.setFilePath("456.pdf")
Paper1.updatePaperName("chentoukong jiagong jingdu fenxi")
Paper1.updatePaperUsedLanguage(2)
Paper1.paperDataOutput()
xmlFileTest1.inputPaperData(Paper1)


Paper1.paperPublishTime="1988-12-23"
xmlFileTest1.inputPaperData(Paper1)

Paper0.publicationLevel=2
xmlFileTest1.inputPaperData(Paper0)

xmlFileTest1.saveXmlFile("testXmlFile5.xml")        
"""



