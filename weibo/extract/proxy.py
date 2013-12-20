# -*- coding: utf-8 -*-
#/usr/bin/env python

from urllib import quote
import time
import os
__version__ = '1.0'
__author__ = 'http://weibo.com/wtmmac'

'''
Demo for sinaweibopy
主要实现token自动生成及更新
适合于后端服务相关应用
'''
from weibo import APIClient

import sys, os, urllib, urllib2
from http_helper import *
from retry import *
try:
    import json
except ImportError:
    import simplejson as json

# setting sys encoding to utf-8
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# token file path
save_access_token_file  = 'access_token.txt'
file_path = os.path.dirname("/home/awen/weibo/weibo/extract/") + os.path.sep
access_token_file_path = file_path + save_access_token_file


def userinfo():
    filedir=os.path.dirname('/home/awen/weibo/weibo/extract/')+os.path.sep
    file_name='apiinfo'
    files=filedir+file_name
    f=open(files,'r')
    user={}
    i=1
    for line in f.readlines():
        a=line.split(';')
        info={}
        info['APP_KEY']=a[0]
        info['APP_SECRET']=a[1]
        info['CALLBACK_URL']=a[2]
        info['USERID']=a[3]
        info['USERPASSWD']=a[4]
        user[i]=info
        i +=1
    return user

def getclient(user,i):
    client=APIClient(app_key=user[i]['APP_KEY'],app_secret=user[i]['APP_SECRET'],redirect_uri=user[i]['CALLBACK_URL'])
    return client
#client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

def make_access_token(user,i,client,ip,port):
    '''请求access token'''
    params = urllib.urlencode({'action':'submit','withOfficalFlag':'0','ticket':'','isLoginSina':'', \
        'response_type':'code', \
        'regCallback':'', \
        'redirect_uri':user[i]['CALLBACK_URL'], \
        'client_id':user[i]['APP_KEY'], \
        'state':'', \
        'from':'', \
        'userId':user[i]['USERID'], \
        'passwd':user[i]['USERPASSWD'], \
        })

    login_url = 'https://api.weibo.com/oauth2/authorize'

    url = client.get_authorize_url()
    content = urllib2.urlopen(url)
    if content:
        #headers = { 'Referer' : url }
        #这是我做的一些修改，防止爬词被服务器察觉
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0','Referer':url}  
        request = urllib2.Request(login_url, params, headers)
        ip1=ip[i-1]
        port1=port[i-1]
        proxy='http://'+ip1+':'+port
        proxy_support = urllib2.ProxyHandler({'http':proxy}) 
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)  
        urllib2.install_open(opener)
        #opener = get_opener(False)
        #urllib2.install_opener(opener)
        try:
            f = opener.open(request)
            print f.headers.headers
            return_callback_url = f.geturl()
            # print f.read()
        except urllib2.HTTPError, e:
            return_callback_url = e.geturl()
        # 取到返回的code
        code = return_callback_url.split('=')[1]
    #得到token
    token = client.request_access_token(code)
    save_access_token(token)

def save_access_token(token):
    '''将access token保存到本地'''
    f = open(access_token_file_path, 'w')
    f.write(token['access_token']+' ' + str(token['expires_in']))
    f.close()

@retry(1)
def apply_access_token(user,i,client,ip,port):
    '''从本地读取及设置access token'''
    try:
        token = open(access_token_file_path, 'r').read().split()
        if len(token) != 2:
            make_access_token(user,i,client)
            return False
        # 过期验证
        access_token, expires_in = token
        try:
            client.set_access_token(access_token, expires_in)
        except StandardError, e:
            if hasattr(e, 'error'): 
                if e.error == 'expired_token':
                    # token过期重新生成
                    make_access_token(user,i,client)
            else:
                pass
    except:
        make_access_token(user,i,client)
    
    return False
#测试一下接口能否调用
def updateweibo(add):
    #info =raw_input('输入发布的微博信息:')
    update=client.post.statuses__update(status=add,lat=33.1232,long=113.12322)

    
#获取某个地点，然后查找当前地点的用户信息
def add_timeline(add,client):
    a=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    file=add+a+'.txt'
    print file
    filedir=os.path.dirname('/home/awen/weibo/weibo/forum/')+os.path.sep
    file_out=filedir+file
    print file_out
    f=open(file_out,'a')
    #add=quote(add)
    address=client.get.location__geo__address_to_geo(address=add)
    dic=dict(address.geos[0])
    longitude=dic['longitude']    #得到地点对应的经纬度信息
    latitude = dic['latitude']
    latlong={}
    i=1
    nowtime=time.time()
    yestime=time.time()-24*60*60
    for i in range(0,5):
        nearby=client.get.place__nearby_timeline(lat=latitude,long=longitude,count=20,range=2000,starttime=yestime,endtime=nowtime,page=i+1)
        for st in nearby.statuses:
            if st.geo != None:
                a=st.geo.coordinates[0]
                b=st.geo.coordinates[1]
                cs=str(b)+','+str(a)
                locations = client.get.location__geo__geo_to_address(coordinate=cs)
                dic=dict(locations.geos[0])
                """
                c={}
                c['lat']=st.geo.coordinates[0]
                c['longs']=st.geo.coordinates[1]
                c['info']=st.text
                c['address']=dic['address']
                latlong[i]=c
                i +=1
                """
                f.write("%s;%s;%s;%s;%s;%s;%s\n"%(st.user.id,st.id,st.created_at,st.text,st.geo.coordinates[0],st.geo.coordinates[1],dic['address']))
        time.sleep(5)
    f.close()
    return file_out


def get_address(coor):
    locations=client.get.location__geo__geo_to_address(coordinate=coor)
    dic=dict(locations.geos[0])
    return dic['address']
def get_geo(add):
    address =client.get.location__geo__address_to_geo(address=add)
    dic = dict(address.geos[0])
    return dic

if __name__ == "__main__":

    """
    apply_access_token()
    add="黑龙江省哈尔滨市"
    updateweibo(add)
    print opener
    #add=raw_input('输入地点:')
    #add_timeline(add)
    """
    ip=['58.242.249.14','183.136.221.6']
    port=['18186','3128']
    user=userinfo()
    for count in range(0,len(user)):
        i=count+2
        client=getclient(user,i)
        apply_access_token(user,i,client,ip,port)
        add='黑龙江省哈尔滨市'
        add_timeline(add,client)
        time.sleep(10)
        break

        

    
        
