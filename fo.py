#!/usr/bin/env python
#-*- coding:utf-8 -*-

#-------------------------------------------
# Designer  : free.Won <freefis@Gmail.com>  
# Licence   : License on GPL Licence
# Archieved : Mar 2nd 2009  
#-------------------------------------------



import os
import commands
import simplejson

ROOT = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )



def get_all_file(dir):
    """ """
    all_file = {}
    print "walking whole dir..."
    for root, dirs, files in os.walk(dir):
        for name in files:
            abs_path = os.path.join(root, name)

            if os.path.basename(abs_path) == "config.php":
                continue
            if os.path.getsize(abs_path) == 0:
                continue

            ins_path = "/webim/" + (abs_path.split("/webim/"))[1]
            md5 = ( commands.getoutput("md5sum " + abs_path).split(" ") )[0]
            all_file[ins_path] = {"abs_path":abs_path,"md5":md5}
    return all_file


def all_to_temp(all_diff_list):
    for abs_path in all_diff_list:
        cp(abs_path, ROOT+"/temp_all")






def basic_diff(new,old):
    public = []
    for rel_path in new.keys():
        try:
            # filepath has not changed
            if new[rel_path]['md5']  !=  old[rel_path]['md5']:
                # ensure to download
                public.append( new[rel_path]['abs_path'] )
        except:
            # filepath has changed
            public.append( new[rel_path]['abs_path'] )
    return public
            


def mkdir(rel_path):
    dir = os.path.join(ROOT,rel_path)
    try:
        os.mkdir(dir)
    except OSError:
        pass

def echo_file(content , rel_path):
    path = os.path.join(ROOT,rel_path)
    handle = open(path,"wb")
    handle.write(content)
    handle.close()

def cp(rel_frompath,rel_topath):
    #cmd = "cp "+ os.path.join(ROOT,rel_frompath) + " " + os.path.join(ROOT,rel_topath)
    cmd = "cp "+ os.path.abspath(rel_frompath) + " " + os.path.abspath(rel_topath)
    cmd = cmd.replace("py_sync/","")
    print cmd
    os.system(cmd)



def make_file_from_db(QuerySet):
    for Query in QuerySet:
        pathindex = simplejson.loads(Query['pathindex'])
        for install_path in pathindex.keys():
            copy_path = os.path.join( "new_version",install_path )
            filename = os.path.basename(copy_path)
            cp(copy_path,"temp_all/"+filename)


def update_all_version(QuerySet):
    for Query in QuerySet:
        pathindex = Query['pathindex']
        version = Query['version']

        mkdir( "version_"+version )
        # update index
        echo_file(pathindex,"version_"+version+"/index")
        # copy file from temp_all
        for abs_path in simplejson.loads(pathindex):
            filename = os.path.basename(abs_path)
            cp("temp_all/"+filename,"version_"+version+"/"+filename")     
            



if __name__ == '__main__':
    new = get_all_file("new_version")
    old = get_all_file("old_version")
    pub = compare(new,old)
    make_file(pub)

    pub_file_list =  [ one['abs_path'] for one in pub.values()]

    dbapi = Mysql(host="localhost",user="root",passwd="1",db="nextim")
    dbapi.update_index(pub_file_list)
