import scrapy  # 导入 Scrapy 库，用于构建爬虫
from dmbj.items import DmbjItem  # 导入自定义的 Item 类
import re  # 导入正则表达式模块
import os  # 导入操作系统模块
from copy import deepcopy  # 导入深拷贝函数
from scrapy_redis.spiders import RedisSpider  # 导入 Scrapy-Redis 中的 RedisSpider 类


# 创建一个名为 DmSpider 的 Scrapy 爬虫类，继承自 RedisSpider
class DmSpider(RedisSpider):
    name = 'dm'  # 爬虫的名称
    redis_key = 'daomu_key'  # 指定 Redis 的键名，从中读取起始 URL
    # allowed_domains = ['daomubiji.com']  # 允许爬取的域名
    # start_urls = ['http://daomubiji.com/']  # 起始 URL 列表

    # 解析函数，用于处理响应并提取数据
    def parse(self, response):
        a_list = response.xpath('//li[contains(@id, "menu-item")]/a')
        for a in a_list:
            # 创建一个 DmbjItem 实例
            item = DmbjItem()
            # 一级标题
            s = a.xpath('./text()').get()
            # 二级 url
            second_url = a.xpath('./@href').get()
            # 使用正则表达式替换一级标题中的特殊字符为下划线
            item['first_title'] = re.sub(r'[\\：<>*? ]', "_", s)
            # 构造一级标题的文件夹路径
            dir_path = r"小说/{}".format(item['first_title'])
            # 创建之前一定要做判断，如果文件夹不存在，则创建
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            # 构造二级页面，使用 parse_article 方法处理
            yield scrapy.Request(
                url=second_url,
                meta={'item': item},  # 将 item 传递给下一个回调函数
                callback=self.parse_article
            )

    # 解析二级页面
    def parse_article(self, response):
        # 从响应的 meta 中获取之前传递的 item 对象
        item = response.meta.get('item')
        # 三级 url，章节标题
        a_lst = response.xpath('//article/a')
        for a in a_lst:
            # 存储章节标题到 item 对象
            item['second_title'] = a.xpath('./text()').get()
            # 三级 url
            third_url = a.xpath('./@href').get()
            # print(item)
            # 向三级页面发请求
            yield scrapy.Request(
                url=third_url,
                meta={'item': deepcopy(item)},  # 将 item 传递给下一个回调函数
                callback=self.parse_content
            )

    # 解析获取数据内容
    def parse_content(self, response):
        # 从响应的 meta 中获取之前传递的 item 对象
        item = response.meta.get('item')
        # 使用 XPath 选择器提取文章内容的段落
        content_lst = response.xpath('//article[@class="article-content"]/p/text()').getall()
        # 将段落文本连接成一个字符串，并存储到 item 对象
        item['content'] = '\n'.join(content_lst)
        print(item)
        # 将 item 传递给下一个处理管道
        yield item





