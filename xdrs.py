# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib
import re

def get_hash(url, opener):
    c = opener.open(url).read()
    patt = re.compile(r'.*?name="formhash".*?value="(.*?)".*?')
    formhash = patt.search(c)
    if not formhash:
        raise Exception('GET formhash Fail!')
    formhash = formhash.group(1)
    return formhash

class Spider():
	def __init__(self):
		self.front_page_url = 'http://rs.xidian.edu.cn/forum.php'
		self.loginurl = 'http://rs.xidian.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes'
		self.shuiQu_url = 'http://rs.xidian.edu.cn/forum.php?mod=forumdisplay&fid=72&page=1'
		#self.loginurl = 'http://rs.xidian.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LSYxX'
		self.postdata = urllib.urlencode( {
		'username' :'z-kidy' ,
		#'password' :'11457bcfca5888626a7a9c8a6de792fd',
		'password' :'jindi13587741703',
		'quickforward' :'yes',
		'handlekey' :'ls',
		} )
		self.headers   = {
			'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0' 
		}
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

		except urllib2.URLError, e:  
			if hasattr(e, 'code'):    
				print 'The server couldn\'t fulfill the request.'       
				print 'Error code: ', e.code  
			elif hasattr(e, 'reason'):    
				print 'We failed to reach a server.'    
				print 'Reason: ', e.reason    

		else:
			print 'No exception was raised.'

		#response.read()
		#response = self.opener.open(self.front_page_url)
		#fq = open('rs2.html','w')
		#fq.writelines(response.read())  

	def dailySign(self):
		url = 'http://rs.xidian.edu.cn/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'
		formhash = get_hash('http://rs.xidian.edu.cn/plugin.php?id=dsu_paulsign:sign', self.opener)
		print formhash

		data = urllib.urlencode( {
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
		except urllib2.URLError, e:  
			if hasattr(e, 'code'):    
				print 'The server couldnt fulfill the request.'       
				print 'Error code: ', e.code  
			elif hasattr(e, 'reason'):    
				print 'We failed to reach a server.'    
				print 'Reason: ', e.reason    

		else:
			print 'No exception was raised.'
			c = response.read(500)
			print c[c.index('<div class="c"')+15:c.index('</div>')]
			#return '操作成功完成'

			#<form id="qiandao" onkeydown="if(event.keyCode==13){showWindow('qwindow', 'qiandao', 'post', '0');return false}" action="plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1" method="post"></form>	
	
	def Comment(self,url):
		#message=%E6%88%91%E6%98%AF%E6%9D%A5%E6%8B%BF%E9%87%91%E5%B8%81%E7%9A%84&posttime=1416644383&formhash=023d4eb8&usesig=1&subject=++
		#formhash=023d4eb8&handlekey=reply&noticeauthor=&noticetrimstr=&noticeauthormsg=&usesig=1&subject=&message=%E6%88%91%E6%98%AF%E6%9D%A5%E6%8B%BF%E9%87%91%E5%B8%81%E7%9A%84
		data = 'formhash=023d4eb8&handlekey=reply&noticeauthor=&noticetrimstr=&noticeauthormsg=&usesig=1&subject=&message=%E6%88%91%E6%98%AF%E6%9D%A5%E6%8B%BF%E9%87%91%E5%B8%81%E7%9A%84'
		#formhash=023d4eb8&handlekey=reply&noticeauthor=&noticetrimstr=&noticeauthormsg=&usesig=1&subject=&message=%E6%88%91%E6%98%AF%E6%9D%A5%E6%8B%BF%E9%87%91%E5%B8%81%E7%9A%84
		req = urllib2.Request(
			url = url,
			data= data,
			headers = self.headers
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

		else:
			print 'No exception was raised.'
		#print 'sucess Comment'
		#response = self.opener.open(url)

	def guanShui(self):
		req = self.opener.open(self.shuiQu_url)
		decode_req = req.read()
		fq = open('rs.html','w')
		fq.writelines(decode_req)

		#Items = re.findall('.*?<tbody id="no.*?">.*?<tr.*?<td.*?<th.*?<a.*?<a href="(.*?)".*?>(.*?)</a>.*?<span class="xi1">.*?回帖(.*?)</span>.*?</tbody>',decode_req,re.S)
		Items = re.findall(u'.*?<tbody id="no.*?<tr.*?<td.*?<th.*?<a.*?<a href="(.*?)".*?>(.*?)</a>.*?</tbody>',decode_req,re.S)
		#Items = re.findall('.*?<tbody id=.*?<tr.*?<td.*?<th.*?<a.*?<a href="(.*?)".*?>(.*?)</a>.*?<span class="xi.*?>(.*?)</span>.*?</tbody>',decode_req,re.S)
		if Items:
			print 'yes'
			for item in Items:
				print item[0].replace('&amp;','&')
				print item[1]

				#print item[2]
				'''matchObj = re.match('.*回帖.*<strong>(.*?)</strong>.*',item[2])
				if matchObj:
					print item[1]
					#print matchObj.group(1)
					print item[2]
				else:
					print 'no match'
					'''
		else:
			print 'no'


			
'''
		for item in Items:
			print item[0].replace('&amp;','&')
			print item[1]
			print item[2]
'''
#http://rs.xidian.edu.cn/forum.php?mod=viewthread&tid=697085&extra=page%3D1
#http://rs.xidian.edu.cn/forum.php?mod=viewthread&amp;tid=697085&amp;extra=page%3D1

my_spider = Spider()
my_spider.login()

operate = raw_input('''
1. dailySign
2. guanshui
''')


if operate == '1' :
	my_spider.dailySign()
elif operate == '2' :
	my_spider.guanShui()


#url = 'http://rs.xidian.edu.cn/forum.php?mod=post&infloat=yes&action=reply&fid=72&extra=&tid=697678&replysubmit=yes'
#my_spider.Comment(url)

#forum.php?mod=post&infloat=yes&action=reply&fid=72&extra=&tid=697746&replysubmit=yes
