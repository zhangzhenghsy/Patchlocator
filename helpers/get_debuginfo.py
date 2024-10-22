import os
import sys
from sym_table import Sym_Table
import subprocess
import time
from multiprocessing import Pool
import helper_zz

ADDR2LINE = os.getcwd()+'/helpers/aarch64-linux-android-4.9/bin/aarch64-linux-android-addr2line'

def get_debuginfo(kernelspath):
    print ADDR2LINE
    dirs = os.listdir(kernelspath)
    PATHLIST=[]
    #clear
    for Dir in dirs :
        PATH=kernelspath+'/'+Dir
        print PATH
        if not os.path.exists(PATH+"/vmlinux"):
            continue
        if not os.path.exists(PATH+"/tmp_o"):
            PATHLIST += [PATH]
    p=Pool(20)
    resultlist=p.map(get_debuginfo_1,PATHLIST)
    for element in resultlist:
        print element

def get_debuginfo_1(PATH):
    if not os.path.exists(PATH+"/"+"boot"):
        print 'no binary image in',PATH
        return
    symbletable_path=PATH+"/"+"System.map"
    if not os.path.exists(symbletable_path):
        string1='./ext_sym '+PATH+'/boot > '+PATH+'/System.map'
        result=helper_zz.command(string1)
    image=PATH+"/"+"vmlinux"
    if not os.path.exists(image):
        print 'no vmlinux for',PATH
        return
    print PATH
    dbg_out=False
    symbletable=Sym_Table(symbletable_path,dbg_out=dbg_out)
    addrlist=symbletable.getRaddrs()
    t0=time.time()
    with open(PATH+'/tmp_i','w') as f:
        for (st,ed) in addrlist: 
            for i in range(st,ed,4):
                f.write('%x\n' % i)
    with open(PATH+'/tmp_i','r') as fi:
        with open(PATH+"/tmp_o",'w') as fo:
            subprocess.call([ADDR2LINE,'-afip','-e',image],stdin=fi,stdout=fo)
    t1=time.time()
    return (PATH,(t1-t0),(hex(addrlist[0][0]),hex(addrlist[-1][1])))

if __name__ == '__main__':
    #get_debuginfo()
    get_debuginfo_1(sys.argv[1])
