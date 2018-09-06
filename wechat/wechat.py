#coding=utf8
import json
import re
import matplotlib.pyplot as plt
import itchat
import jieba as jieba

import numpy as np
from PIL import Image
from matplotlib.image import imread
from wordcloud import WordCloud, ImageColorGenerator


def to_msg():
    itchat.auto_login(hotReload=True)
    # itchat.run()
    friends = itchat.get_friends(update=True)[0:]
    # print(friends)
    infos = []
    for friend in friends:
        info = {}
        info['nickName'] = friend['NickName']
        info['userName'] = friend['UserName']
        infos.append(info)
    print(infos)
    # itchat.send('不确定', toUserName = '@27901bf12119ae9dc746c5cb9bffb5c6654edc2643952f36aba4233965db930f')

def my_firend():
    itchat.auto_login(hotReload=True)
    friends = itchat.get_friends(update=True)[0:]
    # itchat.send(u'这是一条测试消息', 'filehelper')
    # print(friends)
    siglist = []
    male = female = others = 0
    for i in friends[2:]:
        sex = i['Sex']
        if(sex == 1):
            male+=1
        elif(sex == 2):
            female+=1
        else:
            others+=1
        signature = i['Signature'].strip().replace("span","").replace("class","").replace("emoji","")
        rep = re.compile("1f\d+\w*|[<>/=]")
        signature = rep.sub("", signature)
        siglist.append(signature)
    text = "".join(siglist)
    total = len(friends[2:])
    # print(total)
    print("男生好友比例 : %.2f%%" % (float(male) / total * 100) + "\n"
        "女生好友比例 : %.2f%%" % (float(female) / total * 100) + "\n"
         "不明性别好友 : %.2f%%" % (float(others) / total * 100))
    wordlist = jieba.cut(text,cut_all=True)

    word_space_split = " ".join(wordlist)
    cover = np.array(Image.open(r'C:\Users\Liu\Pictures\xy.png'))
    my_wordcloud = WordCloud(background_color="white",
                             max_words=2000,
                             mask=cover,
                             max_font_size=60,
                             random_state=42,
                             scale=2,
                             font_path="C:\\Windows\\Fonts\\STXINGKA.TTF").generate(word_space_split)

    image_color = ImageColorGenerator(cover)
    plt.imshow(my_wordcloud.recolor(color_func=image_color))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    my_wordcloud.generate(text)
    my_wordcloud.to_file(r"C:\Users\Liu\Desktop\3.png")

if __name__=='__main__':
    # my_firend()
    to_msg()
