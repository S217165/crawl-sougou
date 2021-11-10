# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import sys
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


def chuli(item):
    adapter = ItemAdapter(item)
    # 在“来源”，"移动端标题"，"标题"，"标签"中都有可能出现\xa0、\u200b、\u3000等符号
    old_au = adapter['来源']
    old_mt = adapter['移动端标题']
    old_bt = adapter['标题']
    # 处理标题：去除标题中的\xa0、\u200b、\u3000
    try:
        if str(adapter['来源']) != "":
            move = dict.fromkeys((ord(c) for c in u"\xa0\u200b\u3000"))
            new = adapter['来源'].translate(move)  # new 是字符串
            adapter['来源'] = new.split('\n')  # 转为列表
            if old_au != adapter['来源'][0]:
                print("\n有问题的的来源", old_au)
                print("处理后的结果", adapter['来源'][0])
        else:
            raise DropItem(f"{item}该项缺乏来源")
    except:
        raise DropItem(f"{item}该项缺乏来源")

    try:
        if str(adapter['移动端标题']) != "":
            move = dict.fromkeys((ord(c) for c in u"\xa0\u200b\u3000"))
            new = adapter['移动端标题'].translate(move)  # new 是字符串
            adapter['移动端标题'] = new.split('\n')  # 转为列表
            if old_mt != adapter['移动端标题'][0]:
                print("\n有问题的的移动端标题", old_mt)
                print("处理后的结果", adapter['移动端标题'][0])
        else:
            raise DropItem(f"{item}该项缺乏移动端标题")
    except:
        raise DropItem(f"{item}该项缺乏移动端标题")

    try:
        if str(adapter['标题']) != "":
            move = dict.fromkeys((ord(c) for c in u"\xa0\u200b\u3000"))
            new = adapter['标题'].translate(move)  # new 是字符串
            adapter['标题'] = new.split('\n')  # 转为列表
            if old_bt != adapter['标题'][0]:
                print("\n有问题的的标题", old_bt)
                print("处理后的结果", adapter['标题'][0])
        else:
            raise DropItem(f"{item}该项缺乏标题")
    except:
        raise DropItem(f"{item}该项缺乏标题")

    return item


class collectBlogsPipeline(object):
    progress = 0

    def open_spider(self, spider):
        self.f = open("数据.csv", "w", encoding='utf-8')

        # 准备 mongodb
        host = spider.settings.get("MONGODB_HOST", "localhost")
        port = spider.settings.get("MONGODB_PORT", 27017)
        db_name = spider.settings.get("MONGODB_NAME", "mydb3")
        collecton_name = spider.settings.get("MONGODB_COLLECTON", "数据")
        # 连接Mongodb,得到一个客户端对象
        self.db_client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库，得到一个数据库对象
        self.db = self.db_client[db_name]
        # 指定集合，得到一个集合对象
        self.db_collecton = self.db[collecton_name]

    def process_item(self, item, spider):
        # pass
        # 显示进度条
        self.progress += 1
        print("\r", end="\r")
        # 4.2是因为函数共运行420次，10是由于进度条显示效果太长，所以改为10，都是通过测试得出的，不能通用
        print("总程序进度: {:.2f}%: ,正在写入数据".format(self.progress / 4.2), "▋" * (self.progress // 10), end="")
        # 刷新缓冲区
        sys.stdout.flush()

        chuli(item)

        # 存入csv
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(content)
        # 存入 mongodb 数据库
        item_dict = dict(item)  # 将item转换成字典
        self.db_collecton.insert_one(item_dict)  # 将数据插入到集合

    def close_spider(self, spider):
        self.f.close()
        self.db_client.close()
