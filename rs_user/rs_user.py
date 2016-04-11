# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import Queue, threading
from models import Person

class Spider():
    def __init__(self, username=None, password=None):
        self.front_page_url = 'http://rs.xidian.edu.cn/'
        self.queue = Queue.Queue()
        self.thread_num = 5       # 线程数
    def get_people_info(self, uid=285095):
        profile_url = self.front_page_url + '/home.php?mod=space&uid=%d&do=profile' % uid
        try:            
            source_code = requests.get(profile_url)
        except Exception, e:
            print e
        
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')
        alert = soup.find(class_='alert_error')    # 用户不存在
        if alert:
            return

        name = soup.find_all('div', class_='pbm mbm bbda cl')[0].find('h2').contents[0].strip()
        active_status_list = soup.find(id='pbbs').find_all('li')
        
        try:
            online_time = int(active_status_list[0].contents[1].split()[0])    # 在线时长
        except Exception, e:
            print e
            return 

        register_time = active_status_list[1].contents[1] + ':00'          # 注册时间
        gender = soup.find_all('ul', class_='pf_l')[1].find_all(text='性别')[0].parent.next_sibling.strip()

        statistics_list = soup.find(id='psts').find_all('li')        
        credits = int(statistics_list[1].contents[1])   # 积分
        gold = int(statistics_list[2].contents[1])      # 金币
        upload = int(statistics_list[3].contents[1])    # 上传量
        download = int(statistics_list[4].contents[1])  # 下载量
        seed = int(statistics_list[5].contents[1])      # 发种数
        rp = int(statistics_list[8].contents[1])        # 人品

        try:
            Person.create(id=uid, name=name, online_time=online_time, register_time=register_time, credits=credits,
            gold=gold, upload=upload, download=download, seed=seed, rp=rp, gender=gender)
            print u'成功获取%d用户' % uid
        except Exception, e:
            print e

    def queue_manager(self):
        if self.queue.qsize < 10:
            start_id = self.queue[-1]
            for uid in xrange(start_id+1, start_id+101):
                self.queue.put(uid)

        while not self.queue.empty():
            uid = self.queue.get()
            self.get_people_info(uid=uid)

    def work_queue(self):
        threads = []

        for uid in xrange(10000):   # 需要一个判断做连续存储
            self.queue.put(uid)
        for i in xrange(self.thread_num):
            thread = threading.Thread(target=self.queue_manager)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        self.queue.join()

        print 'spider finish!'


if __name__ == '__main__':
    spider = Spider()
    spider.work_queue()










