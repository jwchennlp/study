#coding:utf-8
import codecs

from collections import OrderedDict
#定义停用词词典
def stopworddic():
    f=open('./forum/stopword.txt','r')
    stopword={}
    for line in f.readlines():
        id=line.strip()
        stopword[id]=line.strip()
    f.close()
    return stopword

#对文章进行处理，读取词袋，并消除停用词
def eliminatestopword(stopwrod,file_in,file_out):
    wordbag={}
    f=open(file_in,'r')
    for line in f.readlines():
        words=line.split()
        for i in range(0,len(words)):
            if words[i] not in stopword:
                if words[i] in wordbag:
                    wordbag[words[i]] += 1
                else:
                    id=words[i]
                    wordbag[id]=1
        
    #字典排序
    word=OrderedDict(sorted(wordbag.items(),key=lambda t:t[1],reverse =True))
    #输出出现次数最高的20个词
    f=open(file_out,'w')
    count=len(word)
    for i in word:
        if word[i] >=1:
            f.write('%s,%s%s\n'%(i,100*word[i]/float(count),'%'))
        else :
            break
    f.close()                
                


if __name__=="__main__":
    stopword=stopworddic()
    file1_in='./forum/flu.txt'
    file1_out='./forum/word.txt'
    eliminatestopword(stopword,file1_in,file1_out)

    file2_in='./forum/evaluate.txt'
    file2_out='./forum/word_evaluate.txt'
    eliminatestopword(stopword,file2_in,file2_out)
