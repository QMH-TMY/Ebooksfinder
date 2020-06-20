### 兼容系统 
- Linux 
- Mac OS

### 描述 
[[English](./README.md)] 在命令行查找mobi或epub格式电子书内作者提及的书籍，以《》括起的。

### 依赖 
	zipfile
	$ sudo pip3 install zipfile

### 用法1
    $ python3 Ebooksfinder.py ebook.epub 
    $ python3 Ebooksfinder.py ebook.mobi

### 用法2
    或者将Ebooksfinder.py 加入/usr/local/bin/
    $ mv Ebooksfinder.py Ebooksfinder
    $ chmod +x Ebooksfinder
    $ sudo mv Ebooksfinder /usr/local/bin/

    $ Ebooksfinder ebook.epub #直接当命令使用
    $ Ebooksfinder ebook.mobi
