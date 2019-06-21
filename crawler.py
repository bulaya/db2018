import json
import time
import requests
from bs4 import BeautifulSoup
import argparse


class Crawler:
    def __init__(self, start):
        self.name = 201900001 + start
        self.json_list = []
        self.false_list = "制片国家/地区: none\n类型: none\n上映日期: none\n语言: none\n片长: none"

    def get_one_page(self, url):
        s = requests.session()
        s.headers = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        s.keep_alive = False
        response = s.get(url)
        if response.status_code != 200:
            return 0
        movie_list = response.json()
        for movie in movie_list['data']:
            s.keep_alive = False
            res = s.get(movie['url'])
            soup = BeautifulSoup(res.content, 'html.parser')
            content = soup.select('#info')
            info_list = content[0].text.strip().split('\n') if content else self.false_list
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help="start from here, must be a multiple of 20", type=int, default=0)
    parser.add_argument("-y", "--year", help="get the movie of that year", type=str, default="2018")
    args = parser.parse_args()
    # 开始页数
    start = args.start
    if start%20 != 0:
        print("'start' must is a multiple of 20")
        return
    # 年份
    year = args.year
    crawler = Crawler(start)
    while 1:
        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=' + str(start) + '&year_range=' + year + ',' + year
        print(start)
        start += 20
        # 休息60秒
        time.sleep(60)
        if crawler.get_one_page(url) == 0:
            break
    print('success')


if __name__ == '__main__':
    main()
