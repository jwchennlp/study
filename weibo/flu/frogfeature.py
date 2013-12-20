#coding:utf-8

def frogfeature():
    file_dir='/home/awen/weibo/weibo/clusting/forum/'
    file_name='weibo.txt'
    file_path=file_dir+file_name
    f=open(file_path,'r')
    out='frog.txt'
    fileout=file_dir+out
    g=open(fileout,'w')
    for line in f.readlines():
        words=line.split()
        for i in range(0,len(words)):
            if words[i] =='雾' and i<len(words):
                if words[i+1]=='霾':
                    g.write('%s'%(line))
            elif words[i] == '空气' or words[i]=='污染':
                g.write('%s'%(line))
            else :
                a=1
    f.close()
    g.close()


if __name__=="__main__":
    frogfeature()
