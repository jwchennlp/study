#coding:utf-8
import sys,os,jieba
reload(sys)
sys.setdefaultencoding('utf-8')

def word():
    file='nearby_hit.txt'
    file_path=os.path.dirname("/home/awen/weibo/weibo/forum/")+os.path.sep
    file_out="forum_word_"+file
    dire_out=file_path+file_out
    dire=file_path+file
    f=open(dire,'r')
    g=open(dire_out,'w')
    for line in f.readlines():
        sentence=line.split(';')[3]
        sen1=sentence.split()
        sentence=''.join(sen1[:-1])
        seg_list=jieba.cut(sentence,cut_all=False)
        string =' '.join(seg_list)
        g.write('%s\n'%(string))
    g.close()

if __name__=="__main__":
    word()
