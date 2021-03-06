#coding:utf-8

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn import svm

#定义停用词词典
def stopworddic():
    f=open('/home/awen/weibo/weibo/clusting/forum/stopword.txt','r')
    stopword={}
    for line in f.readlines():
        id=line.strip()
        stopword[id]=line.strip()
    f.close()
    return stopword
#去除停用词
def without_stopword(sen,stopword):
    sen1=sen.split()
    sentence=[]
    for word in sen1:
        if word not in stopword:
            sentence.append(word)
    string = ' '.join(sentence)
    return string
            

def tfidf_clf(stopword):
#read in the training forum
    f =open("word_out.txt")
    train = []
    for line in f.readlines():
        info = without_stopword(line,stopword)
        train.append(info)
    print len(train)
    f.close()
#read in the test forum
    f = open("weibo.txt")
    test = []
    for i in f.readlines():
        info=without_stopword(i,stopword)
        test.append(info)
    f.close()
#transform the vector
    vectorizer = TfidfVectorizer(sublinear_tf= True,min_df=0,max_df=1.0,ngram_range=(1,1),smooth_idf=True,use_idf=1,strip_accents=None)

    x=vectorizer.fit_transform(train)
    n_samples,n_features=x.shape
    print n_samples,n_features
    t=vectorizer.transform(test)
    #print 't',test
    label_train = []
   #read in the train_test forum 
    f = open("result.txt")
    
    for i in f.readlines():
        label_train.append(int(i))
        
    f.close()


    clf = LogisticRegression(penalty='l2',dual=True,fit_intercept=False,C=2,tol=1e-9,class_weight=None, random_state=None, intercept_scaling=1.0)
    clf.fit(x,label_train)
    

    print "evaluate the result",clf.score(x,label_train)
    answer = clf.predict(t)
    pro=clf.predict_proba(t)
   # print 'the total accuracy is ',k/len(answer)
    f=open("evaluate.txt","w")
    count=0
    for i in range(0,len(answer)):
	if pro[i][1]>=0.75:
		count=count+1
                f.write('%s'%(test[i]))
    
    f.close()
    print 'count',count,'allcount',len(test)

if __name__=="__main__":
    
    stopword=stopworddic()
    tfidf_clf(stopword)
    
