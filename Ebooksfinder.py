#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Author: Shieber
#    Date: 2019.01.04
#
#                             APACHE LICENSE
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
#                            Function Description
#    automately search all recomended books in an ebook.
#    and save these books into epubname_booklist.txt
#
#    Copyright 2019 
#    All Rights Reserved!

import re,sys
from os import makedirs
from os import walk 
from os import chdir,getcwd
from os import listdir
from shutil  import move  
from shutil  import copy
from zipfile import ZipFile
from os.path    import join 
from os.path    import  isdir
from os.path    import  exists 
from os.path    import  basename 
from send2trash import send2trash


class EPUBbooksfinder():
    '''
        epub,mobi电子书中推荐书籍获取器，通过命令行传入电子书名称
        程序自动查找书中作者推荐的所有以中文书名号《》括起来的书籍。
        通过使用-a命令行参数，自动查找当前目录下的所有电子书推荐书籍。
    '''
    def __init__(self,suffix='_booklist.txt'):
        '''初始化程序运行的信息'''
        self.delimiter = '/'                            #目录分隔符,windows下是\
        self.html_list = []                             #全局变量，保存(x)html的具体路径
        self.epub_name = sys.argv[1]                    #初始化电子书名
        self.suffix    = suffix                         #书单的后缀名,可自行设置
        self.prefix    = self.get_epub_prefix(sys.argv[1]) #电子书前缀名
        self.booklist  = self.prefix + self.suffix      #书单名称

    def get_epub_prefix(self,file_name):
        '''提取电子书或任意文件的前缀名'''
        return file_name.split('.')[0]                  #解压后的文件夹名

    def copy2zipdir(self,zip_dir):
        '''为epub建立同名文件夹,并把电子书拷贝进去'''
        makedirs(zip_dir)
        new_name = zip_dir + self.delimiter +  self.epub_name 
        copy(self.epub_name, new_name)                  

    def rename_epub2zip(self,name):
        '''重命名电子书为zip格式并提取到当前文件夹'''
        prefix = self.get_epub_prefix(name)
        if not prefix: 
            sys.exit(-1)

        zip_name = prefix + '.zip'                      
        if name.endswith('.epub') or name.endswith('.mobi'):
            move(name,zip_name)
            return zip_name
        else:
            return False

    def unzip_file(self,name):
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

    def find_xhtml(self,zipdir):
        '''递归式的查找xhtml文件并添加到列表中'''
        for parent,dirnames,filenames in walk(zipdir):
            for dirname in  dirnames:        
                self.find_xhtml(dirname)
            for filename in filenames:    
                if self.isxhtml(filename):
                    html_file = join(parent,filename)
                    self.html_list.append(html_file)

    def write2booklist(self,books):
        '''将所有匹配到的书籍写入文件，一行一本'''
        with open(self.booklist,'a+') as booklist_Obj:
            for i in range(len(books)):
                booklist_Obj.write(books[i]+ '\n')

    def find_book(self,html_file):
        '''在一个html文件中查找书籍'''
        with open(html_file) as html_Obj:
            html_txt = html_Obj.read()

        book_pat = re.compile(r'(《.*?》)')
        books    = book_pat.findall(html_txt)
        if books:
            self.write2booklist(books)

    def rmduplicate(self):
        '''去除重复记录的书籍'''
        if not exists(self.booklist):
            return                                      #没有则返回

        books = []
        with open(self.booklist) as books_Obj:
            lines = books_Obj.readlines()
            for line in lines:
                book = line.strip('\n')
                books.append(book)

        books = sorted(set(books), key=books.index)     #去重
        with open(self.booklist,'w+') as books_Obj:
            for i in range(len(books)):
                books_Obj.write(books[i]+ '\n')         #再次写入

    def search(self):
        '''功能函数，直接调用这一个就可'''
        if len(sys.argv) != 2:
            print("Usage: python %s [xx.epub|xx.mobi]"%sys.argv[0])
            sys.exit(-1)

        cwd = getcwd()
        zip_dir = self.get_epub_prefix(self.epub_name)  #获取电子书名以创建同名文件夹
        self.copy2zipdir(zip_dir)                       #复制电子书到同名文件夹 

        chdir(zip_dir)                                  #切换到文件夹,开始处理电子书  
        zip_name = self.rename_epub2zip(self.epub_name) #改电子书格式为zip 
        self.unzip_file(zip_name)                       #解压缩zip文件

        for item in listdir('.'):                     
            if isdir(item):                             #是路径就进入查找
                self.find_xhtml(item)                   #查找(x)html文件，核心函数
            if self.isxhtml(item):
                self.html_list.append(item)

        chdir(cwd)                                      #退回当前目录,开始查找书籍任务
        for html_file in self.html_list:
            self.find_book(zip_dir+self.delimiter+html_file) #在(x)html中找书，核心函数  
                                                            
        self.rmduplicate()                              #去除重复记录的书籍,没有则直接返回
        send2trash(zip_dir)                             #删除解压缩得到的文件夹　

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
