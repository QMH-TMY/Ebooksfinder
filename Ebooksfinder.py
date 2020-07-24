#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Author: Shieber
#    Date: 2019.01.04

import sys
import re
import platform
import click
from zipfile import ZipFile
from shutil  import move,copy
from send2trash import send2trash
from os.path import join,isdir,exists,basename 
from os import makedirs,walk,chdir,getcwd,listdir

class EPUBbooksfinder():
    '''
        epub,mobi电子书中推荐书籍获取器，通过命令行传入电子书名称
        程序自动查找书中作者提到的所有以中文书名号《》括起来的书籍。
        -a参数，自动查找当前目录下的所有以中文书名号《》括起来的书籍。
    '''

    #依据系统设定分隔符
    @staticmethod
    def delimiter():
        ostype = platform.system()
        if ostype == "Windows":
            return '\\'
        else:
            return '/'

    def __init__(self, epubName, suffix='.txt'):
        '''初始化程序运行的信息'''
        self.delimiter = EPUBbooksfinder.delimiter()  #目录分隔符,windows下是\
        self.htmlLst   = []                           #全局变量，保存(x)html的具体路径
        self.epubName  = epubName                     #初始化电子书名
        self.suffix    = suffix                       #书单的后缀名,可自行设置
        self.prefix    = self.getPrefix(self.epubName)#电子书前缀名
        self.booklist  = self.prefix + self.suffix    #书单名称
        self.pattern   = re.compile(r'(《.*?》)')     #《xxx》正则匹配式

    def getPrefix(self, ebook):
        '''提取电子书或任意文件的前缀名'''
        return ebook.split('.')[0]                     #解压后的文件夹名

    def copy2zipdir(self, zipDir):
        '''为epub建立同名文件夹,并把电子书拷贝进去'''
        makedirs(zipDir)
        newName = zipDir + self.delimiter +  self.epubName 
        copy(self.epubName, newName)

    def renameEpub2zip(self, ebook):
        '''重命名电子书为zip格式并提取到当前文件夹'''
        prefix = self.getPrefix(ebook)
        if not prefix: 
            sys.exit(-1)

        zipName = prefix + '.zip'                      
        if ebook.endswith('.epub') or ebook.endswith('.mobi'):
            move(ebook, zipName)
            return zipName
        else:
            return False

    def unzip(self, ebook):
        '''解压电子书zip格式,目录名为电子书名'''
        if not ebook:
            sys.exit(-1)

        try:
            with ZipFile(ebook) as obj:
                obj.extractall()
        except Exception as err:
            sys.exit(-1)

    def isXhtml(self, fl):
        '''判断是否是htm, html或xhtml'''
        return fl.endswith('.html') or fl.endswith('.xhtml') or fl.endswith('.htm')

    def findXhtml(self, zipdir):
        '''递归查找所有xhtml文件并添加到列表中'''
        for parent, subfolders, filenames in walk(zipdir):
            for subfolder in subfolders:        
                self.findXhtml(subfolder)
            for filename in filenames:    
                if self.isXhtml(filename):
                    abshtmlname = join(parent, filename)
                    self.htmlLst.append(abshtmlname)

    def findBook(self, html):
        '''在一个html文件中查找书籍'''
        with open(html,'r',encoding='utf-8') as obj:
            data = obj.read()

        books = self.pattern.findall(data)
        if books:
            self.write2booklist(books)

    def write2booklist(self, books):
        '''将所有匹配到的书籍写入文件，一行一本'''
        with open(self.booklist,'a+', encoding='utf-8') as obj:
            for book in books:
                obj.write(book + '\n')

    def rmduplicate(self):
        '''去除重复记录的书籍'''
        if not exists(self.booklist):
            return                                    #没有则返回

        books = set()
        with open(self.booklist,'r',encoding='utf-8') as obj:
            for book in obj.readlines():
                books.add(book)

        with open(self.booklist,'w+',encoding='utf-8') as obj:
            for book in books:
                obj.write(book)                       #再次写入

    def search(self):
        '''实现逻辑'''
        cwd = getcwd()

        self.copy2zipdir(self.prefix)                 #复制电子书到同名文件夹 
        chdir(self.prefix)                            #切换到文件夹,开始处理电子书  
        zipName = self.renameEpub2zip(self.epubName)  #改电子书格式为zip 
        self.unzip(zipName)                           #解压缩zip文件

        for item in listdir('.'):                   
            if isdir(item):                           #是路径就进入查找
                self.findXhtml(item)                  #查找(x)html文件，核心函数
            if self.isXhtml(item):
                self.htmlLst.append(item)

        chdir(cwd)                                    #退回当前目录,开始查找书籍任务

        for html in self.htmlLst:
            self.findBook(self.prefix+self.delimiter+html) #在(x)html中找书，核心函数  
                                                            
        self.rmduplicate()                            #去除重复记录的书籍,没有则直接返回
        send2trash(self.prefix)                       #删除解压缩得到的文件夹　

@click.command()
@click.option('--ebook', default=None, help='Ebook name like xxx.epub/xxx.mobi or all')
def getBookList(ebook):
    if  None == ebook:
        print(f'Usage: {sys.argv[0]} --ebook=xxx.epub')
        sys.exit(-1)

    if 'all' != ebook:
        ebooksfinder = EPUBbooksfinder(ebook)
        ebooksfinder.search()
    else:
        for ebook in listdir('.'):
            if ebook.endswith('.epub') or ebook.endswith('.mobi'):
                ebooksfinder = EPUBbooksfinder(ebook)
                ebooksfinder.search()

if __name__ == "__main__":
    getBookList()
