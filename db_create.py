#coding=utf-8
#!/home/purplemaple/py2/microblog/flaskt/bin/python2.7

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI ,SQLALCHEMY_MIGRATE_REPO )
else:
    api.version_control(SQLALCHEMY_DATABASE_URI ,SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
