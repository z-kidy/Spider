# -*- coding: utf-8 -*-
import urllib2
import re
import urllib      
import cookielib 
import string  

class Spider:
    def __init__(self , id , pwd):
        self.query = True
        self.login_url = 'http://wlsy.xidian.edu.cn/PhyEws/default.aspx'
        self.score_url = 'http://wlsy.xidian.edu.cn/PhyEws/student/select.aspx'
        self.cookieJar = cookielib.CookieJar()                                      # 初始化一个CookieJar来处理Cookie的信息  

        self.postdata  = urllib.urlencode({  
        '__VIEWSTATE': '/wEPDwUKMTEzNzM0MjM0OWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFD2xvZ2luMSRidG5Mb2dpbtOya8lT1fzi71oyQgc7Hv73+yvb',
        '__EVENTVALIDATION' : '/wEWBwLprev4CQKckJOGDgKD8YXRCQLJ5dDDBAKVx8n1CQKytMi0AQKcg465CqY+2XXD/g4v/g6yTYN6r/N0zBZo',
        'login1$StuLoginID' :id ,
        'login1$StuPassword' : pwd  ,
        'login1$UserRole': 'Student',
        'login1$btnLogin.x': '26',
        'login1$btnLogin.y' : '11'  ,
        })     # POST的数据 

        self.opener    = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))

    def login(self):
        #自定义一个请求#
        req = urllib2.Request(  
            url  = self.login_url ,  
            data = self.postdata
        )

        try:
            response = self.opener.open(req)

        except urllib2.URLError, e:  
                if hasattr(e, 'code'):    
                    print 'The server couldn\'t fulfill the request.'       
                    print 'Error code: ', e.code    
  
                    elif hasattr(e, 'reason'):    
                    print 'We failed to reach a server.'    
                    print 'Reason: ', e.reason    
                    self.query = False
    
                else:    
                    print 'No exception was raised.'  
    def query_scores(self):
        if self.query:
            #打开成绩查询的页面
            result = self.opener.open(self.score_url)
            decode_result = result.read().decode('gb2312').encode('utf-8')
            myItems = re.findall('<tr>.*?<td.*?<td.*?><a.*?>(.*?)</a></td>.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?><span>(.*?)</span></td>.*?</tr>',decode_result,re.S)
            #获取实验名，成绩
            if myItems:
                print 'query ok'
                for item in myItems:
                    print '实验名: ' + item[0]
                    print '成绩：' + item[1]
            else:
                print 'query error'

if __name__ == '__main__':
    id = raw_input('id:')
    pwd = raw_input('password:')

    my_spider = Spider(id , pwd)
    my_spider.login()
    print 'Enter any key to query'
    raw_input()
    my_spider.query_scores()
