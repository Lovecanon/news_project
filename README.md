##Spider+jieba+Whoosh实现全文搜索

##### 本项目只涉及到工具的使用，并没有啥高深的理论，请放心观看

##流程
* 运行`spider`，爬取网易新闻的新闻标题和正文，保存到MongoDB中
* 创建索引，执行`Retrieval.py`文件中的`create_index(news_list)`方法，传入要索引的新闻
* 运行web目录下的`main.py`，即打开服务器
    * 访问根目录/，键入关键字进行搜索，通过路由访问`main.py`中`index()`方法
    * 然后从创建好的索引目录whoosh_index进行检索，默认检索标题、正文两个字段
    * 返回检索到的数据发送给前台
    * ( ¯(∞)¯ )样式丑了点，嗯..不要在乎那些细节嘛
* 点击文章详情，会通过`_id`在MongoDB数据库中查找

##Whoosh
官方是这样说的：
>Whoosh是一个快速、功能强大的全文索引和搜索库，纯Python实现。程序员可以使用它来轻松地向应用程序和网站添加搜索功能。
Whoosh工作的每一部分都可以扩展或替换，以满足您的需求。

    在开始使用whoosh之前，你需要一个index对象，在你第一次创建index对象时你必须定义一个Schema对象，Schema对象列出了Index的所有域。
一个域就是Index对象里面每个document的一个信息，比如他的题目或者他的内容。一个域能够被索引（就是能被搜索到）或者被存储
（就是得到索引之后的结果，这对于标题之类的索引非常有用）
```python
from whoosh.index import create_in
from whoosh.fields import *

# 创建index对象前必须有个定义好的Schema对象, True表示该字段可以被存储方便查询是拿出来
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
# 创建索引目录，如果之前已经建立好一个索引请使用ix = open_dir("index")
ix = create_in("indexdir", schema)

# 返回一个IndexWriter对象，该对象能够让你将文档添加到索引中
# 1.你不必要把每一个域都填满，whoosh不关系你是否漏掉某个域
# 2.被索引的文本域必须是unicode值，被存储但是不被索引的域（STROED域类型）可以是任何和序列化的对象
# 如果你需要一个既要被索引又要被存储的文本域，你可以索引一个unicode值但是存储一个不同的对象（某些时候非常有用）
writer = ix.writer()
writer.add_document(title=u"First document", path=u"/a", content=u"This is the first document we've added!")
writer.add_document(title=u"Second document", path=u"/b", content=u"The second one is even more interesting!")
writer.commit()  # 提交

from whoosh.qparser import QueryParser
# with表达式来打开搜索对象
with ix.searcher() as searcher:
    # 在搜索文本之前，我们需要一个Searcher对象
    # 如果你想从多个字段中查询，请使用MultifieldParser(['title', 'content'], schema=ix.schema)
    query = QueryParser("content", ix.schema).parse("first")
    results = searcher.search(query)
    print(results[0])
    # {"title": u"First document", "path": u"/a"}
```
##jieba+Whoosh
```python
from jieba.analyse import ChineseAnalyzer
analyzer = ChineseAnalyzer()
schema = Schema(title=TEXT(stored=True, analyzer=analyzer), id=ID(stored=True), content=TEXT(analyzer=analyzer))
ix = create_in('./whoosh_index', schema)
writer = ix.writer()
...
writer.commit()
```

##Whoosh资料

官方文档：http://whoosh.readthedocs.io/en/latest/

* http://blog.sina.com.cn/s/blog_819588bc0101co4b.html
* http://www.cnblogs.com/chang/archive/2013/01/10/2855321.html







