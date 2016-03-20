# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib
import re
import sys

reload(sys) 
sys.setdefaultencoding( "utf-8" )

def get_hash(url, opener):
    c = opener.open(url).read()
    patt = re.compile(r'.*?name="formhash".*?value="(.*?)".*?')
    formhash = patt.search(c)
    if not formhash:
        raise Exception('GET formhash Fail!')
    formhash = formhash.group(1)
    return formhash

class Spider():
    def __init__(self, username=None, password=None):
        self.front_page_url = 'http://rs.xidian.edu.cn/'
        self.loginurl = 'http://rs.xidian.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes'
        self.shuiQu_url = 'http://rs.xidian.edu.cn/forum.php?mod=forumdisplay&fid=72&page=1'
        self.postdata = urllib.urlencode({
        'username': username,
        'password': password,
        'quickforward': 'yes',
        'handlekey': 'ls',
        } )

        # 定义一些头部信息
        self.headers   = {
            'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0' 
        }

        # 保存cookie
        self.cookieJar = cookielib.CookieJar()
        self.opener    = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))

    def login(self):

        req = urllib2.Request(
            url = self.loginurl,
            data= self.postdata,
            headers = self.headers
        )

        try:
            response = self.opener.open(req)
        except Exception, e:  
            print e
        else:
            print 'No exception was raised.'


    def dailySign(self):
        url = 'http://rs.xidian.edu.cn/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'
        formhash = get_hash('http://rs.xidian.edu.cn/plugin.php?id=dsu_paulsign:sign', self.opener)

        data = urllib.urlencode({
                    'formhash' : formhash,
                    'qdxq' : 'kx',
                    'qdmode' : '3',
                    'todaysay' : '',    
                    'fastreply' : '0'
        })

        req = urllib2.Request(
            url = url,
            data = data,
            headers =self.headers
        )

        try:
            response = self.opener.open(req)
        except Exception, e:
            print e  

        else:
            print 'No exception was raised.'
            c = response.read(500)
            print c[c.index('<div class="c"')+15:c.index('</div>')]
            #return '操作成功完成'

  
    def comment(self, tid):
        url = self.front_page_url + 'forum.php?mod=post&action=reply&fid=72&tid=%s&extra=&replysubmit=yes&infloat=yes&handlekey=fastpost' % str(tid)

        formhash = get_hash('http://rs.xidian.edu.cn/forum.php?mod=viewthread&tid=%s'%tid, self.opener)

        data = urllib.urlencode({
                    'formhash': formhash,
                    'message': u'我是来拿点金币的',
                    'usesig': '1',
        })

        req = urllib2.Request(
            url = url,
            data= data,
            headers = self.headers
        )

        try:
            response = self.opener.open(req)
        except Exception, e:  
            print e

        else:
            if '成功' in response.read(500):
                print u'水了一贴'
        

    def guanShui(self):
        req = self.opener.open(self.shuiQu_url)
        decode_req = req.read()
        items = re.findall(u'.*?<tbody id="no.*?<tr.*?<td.*?<th.*?<a.*?<a href="(.*?)".*?>(.*?)</a>.*?</tbody>',decode_req,re.S)
        
        if items:
            for item in items:
                if '散金币' in item[1]:    # topic title
                    print item[1]
                    topic_url = item[0].replace('&amp;', '&')   # topic url
                    tid = re.match(r'.*?tid=(\d+)', topic_url).groups()[0]
                    self.comment(tid)
        else:
            print u'没有散金币主题'
            

if __name__ == '__main__':
    print "Hello! let's login first, Rser!" 
    username = raw_input('username:')
    password = raw_input('password:')

    my_spider = Spider(username=username, password=password)
    my_spider.login()

    operate = raw_input('''
    1. 日常签到
    2. 灌水拿金币
    ''')

    if operate == '1' :
        my_spider.dailySign()
    elif operate == '2' :
        my_spider.guanShui()

