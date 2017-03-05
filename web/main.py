# -*- coding: UTF-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from SearchEngine.Retrieval import WhooshIndex
from news_project import MongoUtils
from bson import ObjectId

app = Flask(__name__)


@app.route('/')
def index():
    search_word = request.args.get('search_word')
    if search_word:
        return render_template('index.html', news_list=idx.search(search_word))
    else:
        return render_template('index.html')


@app.route('/news/<news_id>')
def news(news_id):
    result = coll.find_one({'_id': ObjectId(news_id)})
    print(type(result))
    return render_template('news.html', news=result)

if __name__ == '__main__':
    idx = WhooshIndex()
    coll = MongoUtils.MongoDB().db.news_163


    app.debug = True
    app.run()
