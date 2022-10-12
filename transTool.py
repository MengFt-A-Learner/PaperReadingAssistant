# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 16:32:05 2022

@author: MengFt
"""

import requests
import random
import json
from hashlib import md5
from re import split



class transTool(object):
    def __init__(self):
        #在百度上注册得到的账号
        self.appId='20221011001385250'
        self.appKey='J1qY4VXuCF9QOeumC_R4'
        self.transType=-1   #定义翻译语种，-1是未定义；0是英译汉；1是汉译英
        #英译汉状态下，
        self.transLanguageList=[{"type":"英译汉","from_lang":"en","to_lang":"zh"},
                                {"type":"汉译英","from_lang":"zh","to_lang":"en"},]
        
        self.inputWords=""
        self.outputWords=""
        self.outputWordsList=[]
        print("初始化一个翻译工具，调用了百度的翻译API")
        
    def inputString(self,inputWords,transType=0,deleteWrap=False):
        if transType>=0 and transType<len(self.transLanguageList):
            self.transType=transType
        else:
            return -1
        if deleteWrap==True:
            inputWords=self.wrapDelete(inputWords)
        self.inputWords=inputWords
        
        return 0        
    
    def getTrans(self):
        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path
        #query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'
        query=self.inputWords
        salt = random.randint(32768, 65536)
        tempString=self.appId + query + str(salt) + self.appKey
        self.sign=md5(tempString.encode('utf-8')).hexdigest()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        if self.transType<0:
            print("未定义翻译语言")
            return self.transType
        if self.transType>=len(self.transLanguageList):
            print("翻译语言定义错误，请重新输入transType")
            return self.transType
        from_lang=self.transLanguageList[self.transType]["from_lang"]
        to_lang=self.transLanguageList[self.transType]["to_lang"]
        payload = {'appid': self.appId, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': self.sign}
        try:
            r = requests.post(url, params=payload, headers=headers)
            tempResult=r.json()
            #print(tempResult)
            resultList=tempResult["trans_result"]
            #print("resultList=",resultList)

            self.outputWordsList=[]
            for result in resultList:
                self.outputWordsList.append(result["dst"])
            return self.outputWordsList
            #print("翻译文本段落数：",len(self.outputWordsList))
            #print(self.outputWordsList)
        except Exception as e:
            print("翻译过程出错",e)
    
    def showCurrentTransType(self):
        if self.transType<0:
            print("未定义翻译语言")
            return self.transType
        if self.transType>=len(self.transLanguageList):
            print("翻译语言定义错误，请重新输入transType")
            return self.transType
        print("当前的翻译语种为：", self.transLanguageList[self.transType]["type"])
    
    #删除空行
    def wrapDelete(self,inputString):
        try:
            inputStringList=split(r'[\n]',inputString)
            tempString=""
            for i in inputStringList:
                tempString+=i
            return tempString
        except Exception as e:
            print("删除空行流程失败，错误代码：",e)
            
    def showOutputWordsList(self):
        for i in self.outputWordsList:
            print(i)
        
        
if __name__ == '__main__':
    transTest=transTool()
     
    tempString="In this study, analytical models considering different material and geometry for both single\nand double-lap bolted joints were reviewed for better understand how to select the proper \nmodel for a particular application."
    #tempString=input("请输入文字：")
    transTest.inputString(tempString,transType=0,deleteWrap=True)
    #transTest.inputString("A review on stress distribution, strength and failure of bolted composite joints.",0)
    transTest.getTrans()
    transTest.showOutputWordsList()        
        
        
        
        