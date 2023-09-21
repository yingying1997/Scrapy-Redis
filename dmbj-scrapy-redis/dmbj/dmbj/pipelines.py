# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re  # 导入 re 模块，用于正则表达式操作

# 定义 DmbjPipeline 类
class DmbjPipeline:
    # 处理爬取到的数据项
    def process_item(self, item, spider):
        # 构建保存小说文件的文件夹路径，使用一级标题和二级标题，将特殊字符替换为下划线
        dir_path = r'小说/{}/{}'.format(
            item['first_title'],
            re.sub(r'[\\：<>*? ]', "_", item['second_title'])
        )
        # 构建保存小说内容的文件路径，加上 .txt 后缀
        filename = dir_path + '.txt'
        # 将小说内容写入文件中，使用 UTF-8 编码
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(item['content'])
        # 返回 item 对象，用于后续的处理或保存
        return item