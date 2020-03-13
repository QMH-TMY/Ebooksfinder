#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Author: Shieber
#    Date: 2019.01.04
#

import re,sys
from zipfile import ZipFile
from shutil  import move,copy
from send2trash import send2trash
from os.path import join,isdir,exists,basename 
from os import makedirs,walk,chdir,getcwd,listdir


class EPUBbooksfinder():
    '''
        epub,mobi电子书中推荐书籍获取器，通过命令行传入电子书名称
        程序自动查找书中作者推荐的所有以中文书名号《》括起来的书籍。
        通过使用-a命令行参数，自动查找当前目录下的所有电子书推荐书籍。
    '''
    def __init__(self,suffix='_booklist.txt'):
        '''初始化程序运行的信息'''
        self.delimiter = '/'                          #目录分隔符,windows下是\
        self.htmlLst = []                             #全局变量，保存(x)html的具体路径
        self.epubName = sys.argv[1]                   #初始化电子书名
        self.suffix    = suffix                       #书单的后缀名,可自行设置
        self.prefix    = self.getPrefix(sys.argv[1])  #电子书前缀名
        self.booklist  = self.prefix + self.suffix    #书单名称

    def getPrefix(self,name):
        '''提取电子书或任意文件的前缀名'''
        return name.split('.')[0]                     #解压后的文件夹名

    def copy2zipdir(self,zipDir):
        '''为epub建立同名文件夹,并把电子书拷贝进去'''
        makedirs(zipDir)
        newName = zipDir + self.delimiter +  self.epubName 
        copy(self.epubName, newName)

    def renameEpub2zip(self,name):
        '''重命名电子书为zip格式并提取到当前文件夹'''
        prefix = self.getPrefix(name)
        if not prefix: 
            sys.exit(-1)

        zipName = prefix + '.zip'                      
        if name.endswith('.epub') or name.endswith('.mobi'):
            move(name,zipName)
            return zipName
        else:
            return False

    def unzip(self,name):
        '''解压电子书的zip格式为文件夹,文件夹名为电子书名'''
        if not name:
            sys.exit(-1)
        try:
            with ZipFile(name) as zipObj:
                zipObj.extractall()
        except Exception as err:
            sys.exit(-1)

    def isxhtml(self,name):
        '''判断是否是htm, html或者xhtml,即电子书文档格式'''
        return name.endswith('.html') or name.endswith('.xhtml') or name.endswith('.htm')

    def findXhtml(self,zipdir):
        '''递归式的查找xhtml文件并添加到列表中'''
        for parent,dirnames,filenames in walk(zipdir):
            for dirname in  dirnames:        
                self.findXhtml(dirname)
            for filename in filenames:    
                if self.isxhtml(filename):
                    html = join(parent,filename)
                    self.htmlLst.append(html)

    def write2booklist(self,books):
        '''将所有匹配到的书籍写入文件，一行一本'''
        with open(self.booklist,'a+') as bklstObj:
            for i in range(len(books)):
                bklstObj.write(books[i]+ '\n')

    def findBook(self,html):
        '''在一个html文件中查找书籍'''
        with open(html) as Obj:
            txt = Obj.read()

        patn  = re.compile(r'(《.*?》)')
        books = patn.findall(txt)
        if books:
            self.write2booklist(books)

    def rmduplicate(self):
        '''去除重复记录的书籍'''
        if not exists(self.booklist):
            return                                    #没有则返回

        books = []
        with open(self.booklist) as Obj:
            lines = Obj.readlines()
            for line in lines:
                book = line.strip('\n')
                books.append(book)

        books = sorted(set(books), key=books.index)   #去重
        with open(self.booklist,'w+') as bkObj:
            for i in range(len(books)):
                bkObj.write(books[i]+ '\n')           #再次写入

    def search(self):
        '''功能函数，直接调用这一个就可'''
        if len(sys.argv) != 2:
            print("Usage: python %s [xx.epub|xx.mobi]"%sys.argv[0])
            sys.exit(-1)

        cwd = getcwd()
        zipDir = self.getPrefix(self.epubName)        #获取电子书名以创建同名文件夹
        self.copy2zipdir(zipDir)                      #复制电子书到同名文件夹 

        chdir(zipDir)                                 #切换到文件夹,开始处理电子书  
        zipName = self.renameEpub2zip(self.epubName)  #改电子书格式为zip 
        self.unzip(zipName)                           #解压缩zip文件

        for item in listdir('.'):                   
            if isdir(item):                           #是路径就进入查找
                self.findXhtml(item)                  #查找(x)html文件，核心函数
            if self.isxhtml(item):
                self.htmlLst.append(item)

        chdir(cwd)                                    #退回当前目录,开始查找书籍任务
        for html in self.htmls:
            self.findBook(zipDir+self.delimiter+html) #在(x)html中找书，核心函数  
                                                            
        self.rmduplicate()                            #去除重复记录的书籍,没有则直接返回
        send2trash(zipDir)                            #删除解压缩得到的文件夹　

def main():
    '''主函数，程序入口'''
    if len(sys.argv) < 2:
        base_name = basename(sys.argv[0])
        print("Usage: %s [xx.epub|xx.mobi] or %s -a"%(base_name, base_name))
        sys.exit(-1)

    if  '-a' == sys.argv[1]:
        for item in listdir('.'):
            if item.endswith('.epub') or item.endswith('.mobi'):
                sys.argv[1] = item 
                ebooksfinder = EPUBbooksfinder()
                ebooksfinder.search()
    else:
        ebooksfinder = EPUBbooksfinder()
        ebooksfinder.search()

if __name__ == "__main__":
    main()
