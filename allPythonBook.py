#!/usr/bin/python
# -*- coding:utf-8 -*-
#  book2345.py
#  TestPython
#
#  Created by yangyong on 16/7/22.
#  Copyright © 2016年 yangyong. All rights reserved.
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import urllib
#import urllib.request
import urllib2
import re
import sys
import time


#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    removeSUB = re.compile('<br/>.*?&nbsp;&nbsp;&nbsp;&nbsp;')
    removeNUll = re.compile('&nbsp;&nbsp;&nbsp;&nbsp;')
    removelt = re.compile('&lt;&gt;')
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
    replaceBR2 = re.compile('<br>')
    replaceBRA = re.compile('<br/>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removelt,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.removeSUB,"\n\t",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"",x)
        x = re.sub(self.replacePara,"",x)
        x = re.sub(self.removeNUll,"\n\t",x)
        
        x = re.sub(self.replaceBRA,"\n  ",x)
#        x = re.sub(self.replaceBR2,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
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
        self.defaultTitle = "wgtd"
        #是否写入楼分隔符的标记
        self.floorTag = 1
        self.title = None
        self.pageCount = 1
        self.pageURL = "1.html"
    #传入页码，获取该页帖子的代码
    def getPage(self,pageURL):
        try:
            # 无论如何，请用 linux 系统的当前字符集输出：
            #构建UR
            url = pageURL

            print "getPage " + url
            #request = urllib2.Request(url)
            #response = urllib2.urlopen(request)
            req = urllib2.Request(url)
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
            #headers = { 'User-Agent' : user_agent }
            req.add_header('User-Agent', user_agent )
            response = urllib2.urlopen(req)
            html = response.read().decode('utf-8')
#            print "htm " + html
            #返回UTF-8格式编码内容
            return html
        #无法连接，报错
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print "error " + e.reason
                return None

    #获取小说名称
    def getTitle(self,page):
        #得到标题的正则表达式
        pattern = re.compile('<a href="./" title="(.*?)">',re.S)
        result = re.search(pattern,page)
        if result:
            #如果存在，则返回标题
            print result
            return result.group(1).strip()
        else:
            return None
        
    #获取下一页
    def getNextPage(self,page):
        #获取帖子页数的正则表达式
        pattern = re.compile('<a class="article-page-next" href="(.*?)">.*?</a>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageTitle(self,page):
        #获取帖子页数的正则表达式
        pattern = re.compile('<div class="bookname">.*?<h1>(.*?)</h1>.*?</a>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None
                
    #获 每一页
    def getContent(self,page):
        #匹配所有楼层的内容
        pattern = re.compile('<div id="content">(.*?)</div>',re.S)
#        print page
        items = re.findall(pattern,page)
        contents = []
        for item in items:
#            print item
            content = self.tool.replace(item)
#            print "item ",content
            contents.append(content)
        return contents
# next page
    def getNextPage(self,page):
        #获取帖子页数的正则表达式
#     <a id="pager_next" href="6310647.html" target="_top" class="next">下一章</a> <a rel="nofollow" href="javascript:;" onclick="addBookMark(6306674,11447,'第1116章 马马虎虎');">加入书签</a>

        pattern = re.compile('<a id="pager_next" href="(.*?)" target="_top" class="next">.*?</a>',re.S)
        result = re.search(pattern,page)
        if result:
            return result.group(1).strip()
        else:
            return None
    
    def setFileTitle(self,title):
        if title is not None:
            #写文件 追加
            self.file = open(title + ".txt","a+")
            self.title = title
            #print u"title",self.defaultTitle
        else:
            self.file = open(self.defaultTitle + ".txt","a+")
                    
    def writeData(self,contents):
        for item in contents:
            floorLine = "\n" + "\t\t\t" + self.title + "\n"
#            print u"title line",floorLine
#            self.file.write(floorLine.encode('utf-8'))
                #self.file.write(self.title)
            self.file.write(item.encode('utf-8'))
            self.floor += 1

    def writeTitle(self, title):
        floorLine = "\n" + "\t\t\t" + title + "\n"
#            #print u"title line",floorLine
#            self.file.write(floorLine.encode('utf-8'))
        #self.file.write(self.title)
#            print "lfor ",floorLine
        self.file.write(floorLine.encode('utf-8'))
#            self.floor += 1
    def getBook(self,all):
        try:
#            6295492http://www.xs.la/11_11447/6766460.html
#                    http://www.xs.la/11_11447/6310647.html
#                    http://www.xs.la/11_11447/6312478.html


            print "该小说共有" + str(floorTag) + "章"
            for i in range(0,int(floorTag)):
                a = (i)/float(floorTag)*100
                print "正在写入第" + str(i) + "章数据" + "完成 " + str(a) + " %"
                
                self.pageURL = self.baseURL+ all
                print "pageurl ", self.pageURL
                
                page = self.getPage(self.pageURL)
                all = self.getNextPage(page)
                print "next page ",all
#                self.pageURL = self.getNextPage(page)
                if self.pageURL == 'index.html':
                    print "end"
                    return;
                title = self.getTitle(page)

                print "title url" + title
                try:
                    self.setFileTitle(title)
                    contents = self.getContent(page)
                    
                    pagetitle = self.getPageTitle(page)
                    print "tite ",pagetitle
                    if pagetitle != None:
                        self.writeTitle(pagetitle)
                
                    self.writeData(contents)
                    time.sleep(8)
                except IOError,e:
                    all = i
                    continue
                finally:
                    print "next"
        except IOError,e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"

    def getBookPage(self,page):
        #匹配所有楼层的内容
        pattern = re.compile('<a href="(.*?)">.*?<img',re.S)
#        print page
        items = re.findall(pattern,page)
        # contents = []
#         for item in items:
# #            print item
#             content = self.tool.replace(item)
        print "item ",items
#             contents.append(content)
        return items

    def  getBookFirstPage(self,page):

        pattern = re.compile('<dd>.*?<a.*?href="(.*?)">',re.S)
        page = re.findall(pattern,page)
        # contents = []
        for item in page:
            print " item " + item
#             content = self.tool.replace(item)

#             contents.append(content)
            return item

    def getFirstBookTitlePage(self,bookUrl):
        try:
        
            url = self.baseURL+ bookUrl
            print "getFirstBookTitlePageurl ",url
            page = self.getPage(url)
            firstUrl = self.getBookFirstPage(page)
            print "firstUrl ",firstUrl
            return firstUrl
        except Exception as e:
            raise
        else:
            pass
        finally:
            pass
        return

    def start(self):
        #indexPage = self.getPage(self.pageURL)
        #self.pageURL = self.getNextPage(indexPage)
        #title = self.getTitle(indexPage)
        #self.setFileTitle(title)
        if self.pageURL == None:
            print "URL已失效，请重试"
            return

        try:
#            6295492http://www.xs.la/11_11447/6766460.html
#                    http://www.xs.la/11_11447/6310647.html
#                    http://www.xs.la/11_11447/6312478.html

            all = "/newclass/1/1.html"
            
            pageURL = self.baseURL+ all
            print "pageurl ", pageURL
            
            page = self.getPage(pageURL)
            items = self.getBookPage(page)
            n = 1;
            for item in items:    
                n=n+1
                if n==2:
                    continue
                bookUrl = self.getFirstBookTitlePage(item)
                print " over " + bookUrl
               
                bookMainUrl = bookUrl[1:11]
                detailUrl = bookUrl[12:]
                self.baseURL = self.baseURL+ "/"+bookMainUrl+"/";
                print "bookMainUrl " + bookMainUrl + '\n' + " detailUrl " + detailUrl

                self.getBook(detailUrl)
            print " over "

        except IOError,e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"
       # self.getBook()

baseURL = "http://www.xs.la"
#http://www.xs.la/11_11447/6295437.html
#http://www.xs.la/11_11447/6295438.html

#floorTag = raw_input("爬虫章节是否输入\n")
floorTag = 2000
bdtb = BDTB(baseURL,floorTag)
bdtb.start()
