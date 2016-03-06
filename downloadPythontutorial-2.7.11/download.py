# -*- coding:utf-8 -*-
import os
import codecs
import requests
import chardet
root_url = "http://www.pythondoc.com/pythontutorial27/_sources/"

path_list = """index.html
appetite.html
interpreter.html
introduction.html
controlflow.html
datastructures.html
modules.html
inputoutput.html
errors.html
classes.html
stdlib.html
stdlib2.html
whatnow.html
interactive.html
floatingpoint.html
appendix.html"""

path_list = path_list.split("\n")

save_dir = "/data/www/downloadPythontutorial-2.7.11/"

for path in path_list:
    url = "{0}{1}.txt".format(root_url, path[:-5])
    print url
    resp = requests.get(url).content
    f = codecs.open("{0}{1}.rst".format(save_dir, path[:-5]), 'w')
    f.write(resp)
    f.close()

print "--------end---------"


