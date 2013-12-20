#coding:utf-8

import glob
import jieba
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   

def getfile():
    file_path='/home/awen/weibo/weibo/forum/*.txt'
    #读取目录下的所有文件，并存入列表中
    file_list=glob.glob(file_path)
    weibo=[]
    for files in file_list:
        data=open(files,'r').read()
        if len(data) !=0:
            f=open(files,'r')
            for line in  f.readlines():
                infos=line.split(';')
                if len(infos)>=4:
                    info= infos[3]
                    weibo.append(info)
            f.close()
    print len(weibo),len(file_list)
    #分词
    f=open('weibo.txt','w')
    for sen in weibo:
        sen1=sen.split()
        sentence=''.join(sen1[:-1])
        seg_list=jieba.cut(sentence,cut_all=False)
        string = ' '.join(seg_list)
        f.write('%s\n'%(string))
    f.close()

if __name__=="__main__":
    getfile()
    
