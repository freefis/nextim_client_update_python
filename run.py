#!/usr/bin/env python
#-*- coding:utf-8 -*-

#-------------------------------------------
# Designer  : free.Won <freefis@Gmail.com>  
# Licence   : License on GPL Licence
# Archieved : Mar 2nd 2009  
#-------------------------------------------


import sys
import simplejson
import os
import fo,db

_abspath = os.path.abspath(__file__)
ROOT = os.path.dirname( os.path.dirname( _abspath ) )


latest_version = sys.argv[1]

os.system("rm -rf version_*")
fo.mkdir("temp_all")

#compare and generate  diff dict.
new = fo.get_all_file(ROOT+"/new_version")
old = fo.get_all_file(ROOT+"/old_version")
basic_diff_list = fo.basic_diff(new,old)
all_diff_list   = fo.basic_diff(new,{})



fo.all_to_temp(all_diff_list)
db.update_all_index(all_diff_list)
sys.exit()


# sync db
db.pub_new(latest_version)    
db.update_index(latest_version,basic_diff)
                              

QuerySet = db.get_all()
for Query in QuerySet:
    if Query['pathindex'] != "[]":
        try:
            os.mkdir("version_"+Query["version"])
        except OSError:
            pass

# generate & copy files  
print QuerySet
fo.make_file_from_db(QuerySet)
fo.update_all_version(QuerySet)
