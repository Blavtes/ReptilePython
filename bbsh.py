#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    removeNUll = re.compile('&nbsp;')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.removeNUll,"",x)
        x = re.sub(self.removeExtraTag,"\n",x)
       #strip()将前后多余内容删除
        return x.strip()

#百度贴吧爬虫类
class BDTB:

    #初始化，传入基地址，是否只看楼主的参数
    def __init__(self,baseUrl,floorTag):
        #base链接地址
        self.baseURL = baseUrl
        #HTML标签剔除工具类对象
        self.tool = Tool()
        #全局file变量，文件写入操作对象
        self.file = None
        #楼层标号，初始为1
        self.floor = 1
        #默认的标题，如果没有成功获取到标题的话则会用这个标题
        self.defaultTitle = "不败战神"
        #是否写入楼分隔符的标记
        self.floorTag = 1
        self.title = None
        self.pageCount = 1
        self.pageURL = '17368292.html'
    #传入页码，获取该页帖子的代码
    def getPage(self,pageURL):
        try:
            #构建URL
            url = self.baseURL+ pageURL
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #返回UTF-8格式编码内容
            return response.read().decode('gbk')
        #无法连接，报错
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接网站,错误原因",e.reason
                return None

    #获取帖子标题
    def getTitle(self,page):
        #得到标题的正则表达式
        pattern = re.compile('<dd>.*?<h1>(.*?)</h1>.*?</dd>',re.S)
        result = re.search(pattern,page)
        if result:
            #如果存在，则返回标题
            return result.group(1).strip()
        else:
            return None
    
    #获取帖子一共有多少页
    def getNextPage(self,page):
        #获取帖子页数的正则表达式
        pattern = re.compile('<h3>.*?<a.*?>.*?</a>.*?<a.*?>.*?</a>.*?<a href="(.*?)">.*?</a>.*?</h3>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    #获 每一页
    def getContent(self,page):
        #匹配所有楼层的内容
        pattern = re.compile('<dd id="contents.*?>(.*?)</dd>',re.S)
        items = re.findall(pattern,page)
        contents = []
        for item in items:
            content = "\n"+self.tool.replace(item)+"\n"
            contents.append(content)
        return contents

    def setFileTitle(self,title):
        if self.defaultTitle is not None:
            self.file = open(self.defaultTitle + ".txt","a+")
            self.title = title
        #print u"title",self.defaultTitle
        else:
            self.file = open(self.defaultTitle + ".txt","a+")

    def writeData(self,contents):
        for item in contents:
            floorLine = "\n" + self.title + "\n"
            #print u"title line",floorLine
            self.file.write(floorLine.encode('utf-8'))
            #self.file.write(self.title)
            self.file.write(item.encode('utf-8'))
            self.floor += 1

    def start(self):
        #indexPage = self.getPage(self.pageURL)
        #self.pageURL = self.getNextPage(indexPage)
        #title = self.getTitle(indexPage)
        #self.setFileTitle(title)
        if self.pageURL == None:
            print "URL已失效，请重试"
            return
        try:
            print "该小时共有" + str(floorTag) + "章"
            for i in range(1,int(floorTag)+1):
                a = i/float(floorTag)*100
                print "正在写入第" + str(i) + "章数据" + "完成 " + str(a) + " %"
                page = self.getPage(self.pageURL)
                self.pageURL = self.getNextPage(page)
                if self.pageURL == 'index.html':
                    print "end"
                    return;
                title = self.getTitle(page)
                self.setFileTitle(title)
                print u"page url" + self.pageURL
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError,e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"

baseURL = 'http://www.23wx.com/html/27/27736/'
#floorTag = raw_input("爬虫章节是否输入\n")
floorTag = 1000
bdtb = BDTB(baseURL,floorTag)
bdtb.start()  
