# coding=utf-8
# !/home/purplemaple/py2/microblog/flaskt/bin/python
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# basedir = '/home/purplemaple/py2/microblog/app'
# app.config['SQLALCHEMY_TRACK_MODFICATIONS'] = True

# make a language pack
LANGUAGES = {
    'en': 'English',
    'es': 'Espanish',
    'zh': 'China'
}

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'GOOGLE', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

WHOOSH_BASH = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_respository')
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5

# mail server settings
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USER_SSL = False
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
# ADMINS = ['a4512046+flasktest-microblog@gmail.com']
ADMINS = ['a45120466@163.com']
# pagination:spilt into some pages
POSTS_PER_PAGE = 3

# because of none avaliable trans service,so this will ct off.
# translate set (using MS translator)
# MS_TRANSLATOR_CLIENT_ID =''#enter your MS translator app id here
# MS_TRANSLATOR_CLIENT_SECRET = '' #enter your MS translator app secret here.
