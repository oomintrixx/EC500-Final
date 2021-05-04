from flask import render_template, request, flash, redirect, url_for
from . import main
from ..models import File, User
from .. import db
from ..file.file_upload_helper import _generateText, convert_binary
from .forms import SearchForm, NewsForm
from datetime import datetime
from newsapi import NewsApiClient

APIKEY = 'f9e31e950cd9484ab3fd7b069a3b39f5'
newsapi = NewsApiClient(api_key=APIKEY)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['inputFile']
        file.save(file.filename)
        text = convert_binary(file.filename)
        newFile = File(name=file.filename, data=file.read(), text=text)
        db.session.add(newFile)
        db.session.commit()
        flash('file uploaded sucessfully!')
        return redirect(url_for('main.index'))
    else:
        return render_template('file/file_upload.html')

@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    keywords = None
    if form.validate_on_submit():
        keywords = File.query
        keywords = keywords.filter(File.name.like('%' + form.query.data + '%'))
        keywords = keywords.order_by(File.name).all()
    return render_template('file/file_result.html', form = form, keywords = keywords)

@main.route('/news', methods=['GET', 'POST'])
def news():
    form = NewsForm()
    keyword = None
    #num = int(request.form.get('num'))
    resultlist = []
    num = 15
    if form.validate_on_submit():
        keyword = form.keyword.data
        news = newsapi.get_everything(q=keyword,language='en', sort_by='relevancy')
        for i in range(num):
            result = news['articles'][i]["description"]+'\n'
                ##save_article(news['articles'][i])
            r = {
                "info":"Author: "+news['articles'][i]["author"]+'\n'+"PublishedAt: "+news['articles'][i]["publishedAt"]+'\n'+"Source: "+news['articles'][i]["source"]["name"]+'\n',
                "title":news['articles'][i]["title"],
                "content":result,
                "Url":news['articles'][i]["url"],
                "imgurl":news['articles'][i]["urlToImage"]
                }
            resultlist.append(r)
    return render_template("news.html", result=resultlist, form = form)
