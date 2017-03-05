# -*- coding: UTF-8 -*-
import os
import jieba
import json
from jieba import analyse
from jieba.analyse import ChineseAnalyzer
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import pymongo

# result = jieba.cut_for_search('王巍在先后多次考察齐家文化遗址')
# print(type(result))
# for r in result:
#     print(r)

a = '王巍在先后多次考察齐家文多次化遗址'
index = a.find('多次d')
print(index)