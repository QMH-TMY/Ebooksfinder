### Compatible OS 
- Linux
- Mac OS

### Description  
[[中文版](./README_CN.m)] Command line interface for finding books recommended by author in an ebook(epub or mobi type).

### Requirement 
	need zipfile
	$ sudo pip3 install zipfile

### Usage1
    $ python3 Ebooksfinder.py ebook.epub 
    $ python3 Ebooksfinder.py ebook.mobi

### Usage2
    add Ebooksfinder.py to /usr/local/bin/ as a system command
    $ mv Ebooksfinder.py Ebooksfinder
    $ chmod +x Ebooksfinder
    $ sudo mv Ebooksfinder /usr/local/bin/

    $ Ebooksfinder ebook.epub #use as a cmd
    $ Ebooksfinder ebook.mobi
