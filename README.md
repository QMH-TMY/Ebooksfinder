### Description  
[[中文版](./README_CN.md)] Command line interface for finding books recommended by author in an ebook(epub or mobi type).

### Compatible OS 
- Linux
- Mac OS
- Windows

### Requirement 
	packages zipfile and click are required
	$ sudo pip3 install zipfile
	$ sudo pip3 install click

### Usage1
    $ python3 Ebooksfinder.py --ebook=ebook.epub 
    $ python3 Ebooksfinder.py --ebook=ebook.mobi
    $ python3 Ebooksfinder.py --ebook='all'

### Usage2
    add Ebooksfinder.py to /usr/local/bin/ as a system command
    $ mv Ebooksfinder.py Ebooksfinder
    $ chmod +x Ebooksfinder
    $ sudo mv Ebooksfinder /usr/local/bin/

    $ Ebooksfinder --ebook=ebook.epub #use as a cmd
    $ Ebooksfinder --ebook=ebook.mobi
    $ Ebooksfinder --ebook='all'
