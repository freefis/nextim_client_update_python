#!/usr/bin/env python
#-*- coding:utf-8 -*-

#-------------------------------------------
# Designer  : free.Won <freefis@Gmail.com>  
# Licence   : License on GPL Licence
# Archieved : Mar 2nd 2009  
#-------------------------------------------


import MySQLdb as mysql
import simplejson
import os

class Mysql:
    def __init__(self,host,user,passwd,db):
        self.conn = mysql.Connect(host=host,user=user,passwd=passwd,db=db,charset="utf8")
        self.cursor = self.conn.cursor(cursorclass = mysql.cursors.DictCursor)
        self.cursor.execute("SET NAMES 'utf8'")


    def _put(self,version,pathindex):
        sql = """INSERT INTO  \
                 update_index (version,pathindex) VALUES ('%s','{}') \
                 ON DUPLICATE KEY UPDATE version='%s', pathindex='%s';""" % (version,version,pathindex)
#        print sql
    	self.cursor.execute(sql)
        self.conn.commit()

    def _get_all(self):
        self.cursor.execute("SELECT * FROM update_index;")
        rows =  self.cursor.fetchall()
        return rows

    def pub_new(self,latest_version):
        self._put(latest_version,"{}")

    def update_all_index(self,_all_diff_list):
        """ turn all_diff into JSON """ 
        all_diff_dict = {}
        for abs_path in _all_diff_list:
            basename = os.path.basename(abs_path)

            print abs_path
            download_path = "temp_all/%s" % ( basename )
            install_path  = "webim/"+abs_path.split("/webim/")[1]
            all_diff_dict[install_path] = download_path
        del _all_diff_list

        pathindex = simplejson.loads(all_diff_dict)
        version = "force_update_all"
        print pathindex
        self._put(version,new_pathindex)
        
        

    def upadte_index(self,version,_basic_diff_list):
        basic_diff_dict = {}       
        for abs_path in _basic_diff_list:                   
            basename = os.path.basename(abs_path)

            download_path = "version_%s/%s" % ( version , basename )
            install_path  = "webim/"+abs_path.split("/webim/")[1]
            basic_diff_dict[install_path] = download_path

        del _basic_diff # clean var                                        
        #print basic_diff_dict

        for Query in self._get_all():     
            pathindex = simplejson.loads(Query['pathindex'])
            for install_path in basic_diff_dict.keys():
                pathindex[install_path]  = basic_diff_dict[install_path]

            new_pathindex = simplejson.dumps(pathindex)
            version = Query['version']

            # path====> {"/install/path/":"/download/path/"}
            self._put(version,new_pathindex)


                                       
# for called  while imported
_start =  Mysql(host="localhost",user="root",passwd="1",db="nextim_update")
get_all = _start._get_all
pub_new = _start.pub_new
update_index = _start.upadte_index
update_all_index = _start.update_all_index






if __name__ == '__main__':
    dbapi = Mysql(host="localhost",user="root",passwd="1",db="nextim_update")
    for one in  dbapi.select("SELECT * FROM sites"):
        print one
