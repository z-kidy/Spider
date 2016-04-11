# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from models import Person

class Spider():
    def __init__(self, username=None, password=None):
        self.front_page_url = 'http://rs.xidian.edu.cn/'


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
        
        online_time = int(active_status_list[0].contents[1].split()[0])    # 在线时长
        register_time = active_status_list[1].contents[1] + ':00'          # 注册时间
        gender = soup.find_all('ul', class_='pf_l')[1].find_all('li')[1].contents[1].strip()

        statistics_list = soup.find(id='psts').find_all('li')        
        credits = int(statistics_list[1].contents[1])   # 积分
        gold = int(statistics_list[2].contents[1])      # 金币
        upload = int(statistics_list[3].contents[1])    # 上传量
        download = int(statistics_list[4].contents[1])  # 下载量
        seed = int(statistics_list[5].contents[1])      # 发种数
        rp = int(statistics_list[8].contents[1])        # 人品

        Person.create(id=uid, name=name, online_time=online_time, register_time=register_time, credits=credits,
            gold=gold, upload=upload, download=download, seed=seed, rp=rp, gender=gender)

if __name__ == '__main__':
    spider = Spider()
    spider.people()










