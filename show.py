import pandas as pd
import re
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
import json


def movie_init():
    name = 201900001
    json_list = []
    pd.set_option('display.max_columns', None)
    for i in range(320):
        with open("json/%s.json" % name, 'r', encoding='utf-8') as f:
            json_list.append(json.load(f))
        name += 1
    return pd.DataFrame(json_list)


def rank(movie, name):
    di = {}
    for i in range(0, len(movie)):
        tr = {"title": movie.iloc[i]['title'], "rate": movie.iloc[i]['rate']}
        li = movie.iloc[i][name].split(' / ')
        for j in li:
            if j not in di.keys():
                di[j] = []
                di[j].append(tr)
            else:
                di[j].append(tr)
    print("----" + name + " rank 3----")
    for key, value in di.items():
        sort = sorted(value, key=lambda x: x['rate'], reverse=True)
        print(key)
        for s in range(3 if len(sort) >= 3 else len(sort)):
            print(sort[s]['title'], sort[s]['rate'])
    print("----------END----------")


def paint(movie):
    num = [0] * 12
    for i in range(0, len(movie)):
        for n in re.findall(r"2018-(..)", movie.iloc[i]['date']):
            num[int(n)-1] += 1
    plt.bar(range(1, 13), num)
    plt.title('Release Time Distribution Map')
    plt.show()


def comments(movie):
    for i in range(0, len(movie)):
        votes = int(int(movie.iloc[i]['votes']) / 1000) + 1
        with open('words.txt', 'a', encoding='utf-8') as f:
            for v in range(votes):
                f.write(movie.iloc[i]['title'] + ' ')
    txt = open("words.txt", encoding='utf-8').read()
    ai_mask = np.array(Image.open("img/ai.jpg"))
    wc = WordCloud(background_color='white',
                   width=2080,
                   height=1763,
                   max_words=2000,
                   max_font_size=70,
                   collocations=False,
                   mask=ai_mask,
                   font_path="msyh.ttc")
    wc.generate_from_text(txt)
    img_colors = ImageColorGenerator(ai_mask)
    # 字体颜色为背景图片的颜色
    wc.recolor(color_func=img_colors)
    # 显示词云图
    plt.imshow(wc)
    wc.to_file('test.png')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def main():
    movie = movie_init()
    rank(movie, 'type')
    rank(movie, 'area')
    rank(movie, 'language')
    paint(movie)
    comments(movie)


if __name__ == '__main__':
    main()
