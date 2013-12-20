# -*- coding: utf-8 -*-
#/usr/bin/env python

from urllib import quote
import time
__version__ = '1.0'
__author__ = 'http://weibo.com/wtmmac'

'''
Demo for sinaweibopy
主要实现token自动生成及更新
适合于后端服务相关应用
'''

# api from:http://michaelliao.github.com/sinaweibopy/
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

# weibo api访问配置
APP_KEY = '3734665204'      # app key
APP_SECRET = 'adaaeda524b75c41a27375cf8a4f6246'   # app secret
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html' # callback url 授权回调页,与OAuth2.0 授权设置的一致
USERID = 'hit1093710417@gmail.com'       # 微博用户名                     
USERPASSWD = 'hit200441688'   # 用户密码

# token file path
save_access_token_file  = 'access_token.txt'
file_path = os.path.dirname("/home/awen/weibo/Sina-weibo-api-access-by-python/") + os.path.sep
access_token_file_path = file_path + save_access_token_file

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

def make_access_token():
    '''请求access token'''
    params = urllib.urlencode({'action':'submit','withOfficalFlag':'0','ticket':'','isLoginSina':'', \
        'response_type':'code', \
        'regCallback':'', \
        'redirect_uri':CALLBACK_URL, \
        'client_id':APP_KEY, \
        'state':'', \
        'from':'', \
        'userId':USERID, \
        'passwd':USERPASSWD, \
        })

    login_url = 'https://api.weibo.com/oauth2/authorize'

    url = client.get_authorize_url()
    content = urllib2.urlopen(url)
    if content:
        headers = { 'Referer' : url }
        #这是我做的一些修改，防止爬词被服务器察觉
        #headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
        request = urllib2.Request(login_url, params, headers)
        opener = get_opener(False)
        urllib2.install_opener(opener)
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
def apply_access_token():
    '''从本地读取及设置access token'''
    try:
        token = open(access_token_file_path, 'r').read().split()
        if len(token) != 2:
            make_access_token()
            return False
        # 过期验证
        access_token, expires_in = token
        try:
            client.set_access_token(access_token, expires_in)
        except StandardError, e:
            if hasattr(e, 'error'): 
                if e.error == 'expired_token':
                    # token过期重新生成
                    make_access_token()
            else:
                pass
    except:
        make_access_token()
    
    return False

if __name__ == "__main__":
    apply_access_token()

    # 以下为访问微博api的应用逻辑
    # 以接口访问状态为例
    """
    status = client.get.statuses__public_timeline()
    print type(status)
    f=open("1.txt","w")
    f.write('%s'%(status))
    for st in status.statuses:
        print st.text,st.id,st.user.id,st.created_at
    """
    #下面研究分页的问题
    """
    status = client.get.statuses__friends_timeline(count=50,page=1)
    print type(status)
    print len(status)
    for st in status.statuses:
        print st.text,st.id,st.user.id
    """
    #看一下多分页爬取效果
    #这段不成功...
    """
    f=open('page.txt','w')
    for i in range(1,10):
        print quote('感冒')
        status=client.get.place__pois__search(keyword='感冒',count=50,page=i)
        for st in status.pois:
            print pois.address
    """
    """
    #获取当前登陆用户和好友的位置动态
    f=open('geo.txt','w')
    
    status = client.place__friends_timeline(count=30,page=1)
    for st in status.statuses:
        if st.geo !=None:
            a=st.geo.coordinates[0]
            b=st.geo.coordinates[1]
            c=str(b)+','+str(a)
            locations = client.get.location__geo__geo_to_address(coordinate=c)
            #获取的locations.geos是一个列表，将他转换成字典后获取其中的address
            dic=dict(locations.geos[0])
            f.write("%s;%s;%s;%s;/%s;%s\n"%(st.user.id,st.id,st.created_at,st.text,st.geo.coordinates,dic['address']))
    f.close()
    """
    #精确的经纬度为什么得不到具体的地址，这里测试一下,终于成功了，主要是在参数传递的问题,回到上一步
    """
    a=126.623066
    b=45.737565
    c=str(a)+','+str(b)
    locations =client.get.location__geo__geo_to_address(coordinate=c)
    dic=dict(locations.geos[0])
    print dic['address']
    """
    #接下来我想做的就是获取某个地点，然后查找当前地点用户的信息
    f=open('nearby1.txt','w')
    add="中国黑龙江省哈尔滨市南岗区西大直街92号"
    #add=quote(add)
    address=client.get.location__geo__address_to_geo(address=add)
    dic=dict(address.geos[0])
    longitude=dic['longitude']    #得到地点对应的经纬度信息
    latitude = dic['latitude']
    print longitude,latitude
    nowtime=time.time()
    yestime=time.time()-24*60*60
    for i in range(1,11):
        nearby=client.get.place__nearby_timeline(lat=latitude,long=longitude,count=50,range=5000,starttime=yestime,endtime=nowtime,page=i)
        for st in nearby.statuses:
            if st.geo != None:
                a=st.geo.coordinates[0]
                b=st.geo.coordinates[1]
                c=str(b)+','+str(a)
                locations = client.get.location__geo__geo_to_address(coordinate=c)
                dic=dict(locations.geos[0])
                f.write("%s;%s;%s;%s;/%s;%s\n"%(st.user.id,st.id,st.created_at,st.text,st.geo.coordinates,dic['address']))
    f.close()
        
