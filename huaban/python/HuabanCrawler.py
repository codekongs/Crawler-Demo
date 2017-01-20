#!/usr/bin/env python
# encoding: utf-8
# @author: cc <chai_pengfei@163.com>

import requests
import re
import os
import os.path

class HuabanCrawler():
    """ 抓取花瓣网上的图片 """

    def __init__(self, path):
        """ 在当前文件夹下新建images文件夹存放抓取的图片 """
        self.images = []
        self.path = path
        self.homeUrl = "http://huaban.com/favorite/" + path
        if not os.path.exists('./' + path):
                os.mkdir('./' + path)
    def __load_homePage(self):
        """ 加载主页面 """
        return requests.get(url = self.homeUrl).content

    def __make_ajax_url(self, No):
        """ 返回ajax请求的url """
        return self.homeUrl + "?i5p998kw&max=" + No + "&limit=20&wfl=1"

    def __load_more(self, maxNo):
        """ 刷新页面 """
        return requests.get(url = self.__make_ajax_url(maxNo)).content

    def __process_data(self, htmlPage):
        """ 从html页面中提取图片的信息 """
        prog = re.compile(b'app\.page\["pins"\].*')
        appPins = prog.findall(htmlPage)
        # 将js中的null定义为Python中的None
        null = None
        true = True
        false = False
        if appPins == []:
            return None
        result = eval(appPins[0][19:-1])
        for i in result:
            info = {}
            info['id'] = str(i['pin_id'])
            info['url'] = "http://img.hb.aicdn.com/" + i["file"]["key"] + "_fw658"
            if 'image' == i["file"]["type"][:5]:
                info['type'] = i["file"]["type"][6:]
            else:
                info['type'] = 'NoName'
            self.images.append(info)

    def __save_image(self, imageName, content):
        """ 保存图片 """
        with open(imageName, 'wb') as fp:
            fp.write(content)

    def get_image_info(self, num=20):
        """ 得到图片信息 """
        self.__process_data(self.__load_homePage())
        for i in range(round((num-1)/20)):
            self.__process_data(self.__load_more(self.images[-1]['id']))
        return self.images

    def down_images(self):
        """ 下载图片 """
        print("{} image will be download".format(len(self.images)))
        for key, image in enumerate(self.images):
            print(self.path + ' download {0} ...'.format(key))
            try:
                req = requests.get(image["url"])
            except :
                print('error')
            imageName = os.path.join("./" + self.path, image["id"] + "." + image["type"])
            self.__save_image(imageName, req.content)


if __name__ == '__main__':
    num = input("请输入图片数目")
    path = tuple(open('./path.txt', 'r'))
    for x in range(0, len(path)):
        p = path[x].rstrip('\n');
        # self.homeUrl[x] = "http://huaban.com/favorite/" + p + "/"
        if not os.path.exists('./' + p):
            os.mkdir('./' + p)
        hc = HuabanCrawler(p)
        hc.get_image_info(int(num))
        hc.down_images()
