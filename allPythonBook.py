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
import random

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
agents = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )",
    "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)",
    "Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a",
    "Mozilla/2.02E (Win95; U)",
    "Mozilla/3.01Gold (Win95; I)",
    "Mozilla/4.8 [en] (Windows NT 5.1; U)",
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)",
    "HTC_Dream Mozilla/5.0 (Linux; U; Android 1.5; en-ca; Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; sdk Build/CUPCAKE) AppleWebkit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; htc_bahamas Build/CRB17) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.1-update1; de-de; HTC Desire 1.19.161.5 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-ch; HTC Hero Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; HTC Legend Build/cupcake) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/PLAT-RC33) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1 FirePHP/0.3",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; HTC_TATTOO_A3288 Build/DRC79) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.0; en-us; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-us; T-Mobile G1 Build/CRB43) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari 525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.5; en-gb; T-Mobile_G2_Touch Build/CUPCAKE) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Milestone Build/ SHOLS_U2_01.03.1) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.0.1; de-de; Milestone Build/SHOLS_U2_01.14.0) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522  (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.1; en-us; Nexus One Build/ERD62) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-us; ADR6300 Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.2; en-ca; GT-P1000M Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 3.0.1; fr-fr; A500 Build/HRI66) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/525.10  (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
    "Mozilla/5.0 (Linux; U; Android 1.6; es-es; SonyEricssonX10i Build/R1FA016) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
    "Mozilla/5.0 (Linux; U; Android 1.6; en-us; SonyEricssonX10i Build/R1AA056) AppleWebKit/528.5  (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
]

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
            agent = random.choice(agents)
            user_agent = agent
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
                    # time.sleep(8)
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
            #分类url
            pageURL = self.baseURL+ all
            print "pageurl ", pageURL
            #
            page = self.getPage(pageURL)
            #没本书URL
            items = self.getBookPage(page)
            n = 1;
            for item in items:    
                n=n+1
                if n==2:
                    continue
                bookUrl = self.getFirstBookTitlePage(item)
                print " over " + bookUrl
                #书主URl
                bookMainUrl = bookUrl[1:11]
                #章节URL
                detailUrl = bookUrl[12:]
                #书基本URL
                self.baseURL = self.baseURL+ "/"+bookMainUrl+"/";
                print "bookMainUrl " + bookMainUrl + '\n' + " detailUrl " + detailUrl
                #章节URL 获取内容
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
