# -*- coding: UTF-8 -*-
import jieba
from jieba.analyse import ChineseAnalyzer
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import MultifieldParser
import pymongo
import logging
import os

client = pymongo.MongoClient()
db_news = client.news
news_163 = db_news.news_163
path = os.path.join(os.path.split(__file__)[0], 'whoosh_index')

jieba.initialize()  # 手动初始化


class WhooshIndex(object):
    def __init__(self, index_path=path):
        if not os.path.exists(index_path):
            os.mkdir(index_path)
        self.index_path = index_path

    def search(self, words, count=10, offset=0):
        ix = open_dir(self.index_path)
        parser = MultifieldParser(['title', 'content'], schema=ix.schema)
        news_list = []
        with ix.searcher() as searcher:
            results = searcher.search(parser.parse(words))[offset:count]
            for news in results:
                content = WhooshIndex.seg_content(news['content'], words)
                news_list.append({'title': news['title'], 'content': content, 'id': news['id']})
        return news_list

    def create_index(self, news_list):
        analyzer = ChineseAnalyzer()
        schema = Schema(title=TEXT(stored=True, analyzer=analyzer), id=ID(stored=True),
                        content=TEXT(stored=True, analyzer=analyzer))
        ix = create_in(self.index_path, schema)
        writer = ix.writer()
        index = 0
        for news in news_list:
            writer.add_document(title=news['title'], id=str(news['_id']), content=news['content'])
            index += 1
        writer.commit()
        logging.info('+++Writen %d items to index file' % (index,))

    @staticmethod
    def seg_content(content, words):
        seg_words = jieba.cut_for_search(words)
        for word in seg_words:
            index = content.find(word)
            if index != -1:
                return content[index: index + 100]
        return content[:100]


if __name__ == '__main__':
    index = WhooshIndex()
    # index.create_index(news_163.find())
    ids = index.search('美国  傅莹')
    print(ids)
