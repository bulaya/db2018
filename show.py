import pandas as pd
import re
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
import matplotlib.pyplot as plt
import json
import argparse


def movie_init():
    name = 201900001
    json_list = []
    while 1:
        try:
            with open("json/%s.json" % name, 'r', encoding='utf-8') as f:
                json_dir = json.load(f)
                json_list.append(json_dir)
            name += 1
        except IOError:
            break
    return pd.DataFrame(json_list)


def rank(movie, name):
    di = {}
    for i in range(0, len(movie)):
        tr = {"title": movie.iloc[i]['title'], "rate": movie.iloc[i]['rate']}
        if tr['rate'] == '':
            continue
        try:
            li = movie.iloc[i][name].split(' / ')
        except AttributeError:
            continue
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
            if sort[s]['rate'] != '':
                print(sort[s]['rate'], "  ", sort[s]['title'])
    print("----------END----------")


def paint(movie):
    num = [0] * 12
    for i in range(0, len(movie)):
        try:
            for n in re.findall(r"2018-(..)", movie.iloc[i]['date']):
                num[int(n) - 1] += 1
        except TypeError:
            continue
    plt.bar(range(1, 13), num)
    plt.title('Time Distribution Map')
    plt.show()


def show_image(file_name, width, height, max_font_size, old_image, new_image):
    txt = open(file_name, encoding='utf-8').read()
    ai_mask = np.array(Image.open("img/" + old_image))
    wc = WordCloud(background_color='white',
                   width=width,
                   height=height,
                   max_words=9000,
                   max_font_size=max_font_size,
                   collocations=False,
                   mask=ai_mask,
                   font_path="msyh.ttc")
    wc.generate_from_text(txt)
    img_colors = ImageColorGenerator(ai_mask)
    wc.recolor(color_func=img_colors)
    plt.imshow(wc)
    wc.to_file('img/' + new_image)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def votes(movie):
    with open('text/title.txt', 'a', encoding='utf-8') as f:
        for i in range(0, len(movie)):
            votes = int(int(movie.iloc[i]['votes']) / 1000) + 1
            for v in range(votes):
                f.write(movie.iloc[i]['title'] + ' ')
    show_image('text/title.txt', 4096, 2160, 100, 'ai.png', 'title.png')


def language(movie):
    with open('text/language.txt', 'a', encoding='utf-8') as f:
        for i in range(0, len(movie)):
            try:
                language_list = movie.iloc[i]['language'].split(' / ')
            except AttributeError:
                continue
            for l in language_list:
                f.write(l + ' ')
    show_image('text/language.txt', 1920, 1080, 3000, 'nahan.jpg', 'language.png')


def area(movie):
    with open('text/area.txt', 'a', encoding='utf-8') as f:
        for i in range(0, len(movie)):
            try:
                area_list = movie.iloc[i]['area'].split(' / ')
            except AttributeError:
                continue
            for l in area_list:
                f.write(l + ' ')
    show_image('text/area.txt', 1920, 1080, 2000, 'xk.jpg', 'area.png')


def type(movie):
    with open('text/type.txt', 'a', encoding='utf-8') as f:
        for i in range(0, len(movie)):
            try:
                type_list = movie.iloc[i]['type'].split(' / ')
            except AttributeError:
                continue
            for l in type_list:
                f.write(l + ' ')
    show_image('text/type.txt', 1000, 800, 1000, 'light.png', 'type.png')


def main():
    movie = movie_init()
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rank", help="[type] print type rank 3,"
                                             "[area] print area rank 3,"
                                             "[language] print language rank 3", type=str)
    parser.add_argument("-m", "--map", help="[month] display time distribution map,"
                                            "[votes] display score distribution map,"
                                            "[language] display language distribution map,"
                                            "[area] display area distribution map,"
                                            "[type] display type distribution map", type=str)
    args = parser.parse_args()
    if args.rank:
        rank(movie, args.rank)
    if args.map:
        if args.map == 'month':
            paint(movie)
        elif args.map == 'votes':
            votes(movie)
        elif args.map == 'language':
            language(movie)
        elif args.map == 'area':
            area(movie)
        elif args.map == 'type':
            type(movie)
        else:
            print('python show.py -h 了解一下')


if __name__ == '__main__':
    main()
