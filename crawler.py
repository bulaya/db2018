import json
import time
import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, start):
        self.name = 201900001 + start
        self.json_list = []

    def get_one_page(self, url):
        response = requests.get(url, 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')
        if response.status_code != 200:
            return 0
        movie_list = response.json()
        for movie in movie_list['data']:
            res = requests.get(movie['url'])
            soup = BeautifulSoup(res.content, 'html.parser')
            info_list = soup.select('#info')[0].text.strip().split('\n')
            for i in info_list:
                item = i.split(': ')
                if item[0] == '制片国家/地区':
                    movie['area'] = item[1]
                if item[0] == '类型':
                    movie['type'] = item[1]
                if item[0] == '上映日期':
                    movie['date'] = item[1]
                if item[0] == '语言':
                    movie['language'] = item[1]
                if item[0] == '片长':
                    movie['long'] = item[1]
            votes = soup.find('span', {"property": "v:votes"})
            movie['votes'] = votes.text if votes else "0"
            self.json_list.append(movie)
            filename = '%s.json' % self.name
            with open('json/' + filename, 'w', encoding='utf-8') as f:
                json.dump(movie, f, ensure_ascii=False)
            print(self.name)
            self.name += 1


def main():
    # 开始页数
    start = 0
    # 年份
    year = "2018"
    crawler = Crawler(start)
    while 1:
        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=' + str(start) + '&year_range=' + year + ',' + year
        print(start)
        start += 20
        # 休息30秒
        time.sleep(30)
        if crawler.get_one_page(url) == 0:
            break
    print('success')


if __name__ == '__main__':
    main()
