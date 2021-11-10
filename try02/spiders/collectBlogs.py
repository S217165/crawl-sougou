# -*- coding: utf-8 -*-
import json
import time
import scrapy
from scrapy.exceptions import DropItem

from try02.items import CollectdataItem


def post_detail(response):
    item = response.meta.get('item')
    req = json.loads(response.text)
    authorName, mobileTitle, contentType, title, authorId, authorPic, personalPage, pub_time, img_url, tag_name, originalSource = [], [], [], [], [], [], [], [], [], [], []
    for data in req:
        # 来源
        try:
            authorName.append(data['authorName'])  # 来源
        except:
            print(f"\n\n{data}\n该项缺乏来源\n")
            authorName.append('')
        # 移动端标题
        try:
            mobileTitle.append(data['mobileTitle'])  # 移动端标题
        except:
            print(f"\n\n{data}\n该项缺乏移动端标题\n")
            mobileTitle.append('')
        # 文章类型
        try:
            contentType.append(data['contentType'])  # 文章类型
        except:
            print(f"\n\n{data}\n该项缺乏文章类型\n")
            contentType.append('')
        # 标题
        try:
            title.append(data['title'])  # 标题
        except:
            print(f"\n\n{data}\n该项缺乏标题\n")
            title.append('')
        # 来源_ID
        try:
            authorId.append(data['authorId'])  # 来源_ID
        except:
            print(f"\n\n{data}\n该项缺乏来源_ID\n")
            authorId.append('')
        # 来源图标
        try:
            authorPic.append(data['authorPic'])  # 来源图标
        except:
            print(f"\n\n{data}\n该项缺乏来源图标\n")
            authorPic.append('')
        # 个人网站
        try:
            personalPage.append(data['personalPage'])  # 个人网站
        except:
            print(f"\n\n{data}\n该项缺乏个人网站\n")
            personalPage.append('')
        # 发表时间
        try:
            # 13 位时间戳转换为日期格式字符串
            pub_time.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['publicTime'] / 1000)))  # 发表时间
            print("处理前（13位时间戳）：", data['publicTime'])
            print("处理后（日期格式）：", pub_time[-1])
        except:
            print(f"\n\n{data}\n该项缺乏发表时间\n")
            pub_time.append('')
        # 图片链接
        try:
            img = []
            for i in data['images']:
                if i:
                    img.append(i)
            img_url.append(img)
        except:
            print(f"\n\n{data}\n该项缺乏图片链接\n")
            img_url.append('')
        # 标签
        try:
            tag = []
            for i in data['tags']:
                if i:
                    tag.append(i['name'])
            tag_name.append(tag)
        except:
            print(f"\n\n{data}\n该项缺乏标签\n")
            tag_name.append('')
        # 来源网址
        try:
            originalSource.append(data['originalSource'])  # 来源网址
        except:
            originalSource.append('')
            print(f"\n\n{data}\n该项缺乏来源网址\n")
            # raise DropItem(f"{data}该项缺乏来源网址")

    for i in range(len(authorName)):
        item['来源'] = authorName[i]
        item['移动端标题'] = mobileTitle[i]
        item['文章类型'] = contentType[i]
        item['标题'] = title[i]
        item['来源_ID'] = authorId[i]
        item['来源图标'] = authorPic[i]
        item['个人网站'] = personalPage[i]
        item['发表时间'] = pub_time[i]
        item['图片链接'] = img_url[i]
        item['标签'] = tag_name[i]
        item['来源网址'] = originalSource[i]
        yield item
        # print(item)


class collectBlogsSpider(scrapy.Spider):
    name = 'collectBlogs'
    allowed_domains = ['sohu.com']
    start_urls = ['https://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1460&page=1&size=20']
    # 1460(sceneId): 搜狐新闻时政版块
    # page(>=1&&<=99): 页面数(超过100页网址失效); size(>=1&&<=1000): 页面容量;
    # page * size <=1000: 一次最多查询 1000 条新闻，超过 1000 条内容为空;
    base_urls = "https://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1460&size=20&page="
    page = 1

    # 翻页
    def parse(self, response):
        if self.page < 22:  # 爬取前 21 页, 420 (=20*21) 条新闻
            url = self.base_urls + str(self.page)
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
            item = CollectdataItem()
            request = scrapy.Request(url=url, callback=post_detail, dont_filter=True)
            request.meta['item'] = item
            yield request
            # 显示当前页数
            # print("\n正在爬取第", self.page, "页新闻………………………………………………………………………………")
            self.page += 1
        pass
