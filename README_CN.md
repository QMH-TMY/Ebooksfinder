### 描述 
[[English](./README.md)] 在命令行查找mobi或epub格式电子书内作者提及且以《》括起的书籍。

### 兼容系统 
- Linux 
- Mac OS
- Windows

### 依赖 
	zipfile, click
	$ sudo pip3 install zipfile
	$ sudo pip3 install click

### 用法1
    $ python3 Ebooksfinder.py --ebook=ebook.epub 
    $ python3 Ebooksfinder.py --ebook=ebook.mobi
    $ python3 Ebooksfinder.py --ebook='all'      #提取当前目录下所有电子书内书籍

### 用法2
    将Ebooksfinder.py 加入/usr/local/bin/
    $ mv Ebooksfinder.py Ebooksfinder
    $ chmod +x Ebooksfinder
    $ sudo mv Ebooksfinder /usr/local/bin/

    $ Ebooksfinder --ebook=ebook.epub            #直接当命令使用
    $ Ebooksfinder --ebook=ebook.mobi
    $ Ebooksfinder --ebook='all'
