#coding=utf-8

from coverage import coverage
cov = coverage(branch=True, omit=['flaskt/*', 'tests.py'])
cov.start()

import os
import unittest
from datetime import datetime, timedelta

from config import basedir
from app import app, db
from app.models import User, Post
#from app.translate import microsoft_translate



class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        #make valid nicknames
        n = User.make_valid_nickname('john_123')
        assert n == 'john_123'
        n = User.make_valid_nickname('John_[123]\n')
        assert n == 'John_123'
        #create a user
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        assert u.is_authenticated is True
        assert u.is_active is True
        assert u.is_anonymous is False
        assert u.id == int(u.get_id())

    def test_avatar(self):
        u = User(nickname='john', email='john@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('susan')
        assert nickname == 'susan'
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'
        u = User(nickname=nickname, email='susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 != nickname

    def test_follow(self):
        u1 = User(nickname='john', email='john@example.com')
        u2 = User(nickname='sus', email='sus@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'sus'
        assert u2.followers.count() ==1
        assert u2.followers.first().nickname == 'john'
        u = u1.unfollow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    def test_follow_posts(self):
        #make four users
        u1 = User(nickname='jo', email='jo@example.com')
        u2 = User(nickname='su', email='su@example.com')
        u3 = User(nickname='ma', email='ma@example.com')
        u4 = User(nickname='da', email='da@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        #make 4 posts
        utcnow = datetime.utcnow()
        p1 = Post(body="post from jo", author = u1,timestamp=utcnow + timedelta(seconds=1))
        p2 = Post(body="post from su", author = u2,timestamp=utcnow + timedelta(seconds=2))
        p3 = Post(body="post from ma", author = u3,timestamp=utcnow + timedelta(seconds=3))
        p4 = Post(body="post from da", author = u4,timestamp=utcnow + timedelta(seconds=4))
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.commit()
        #set up the followers
        u1.follow(u1)
        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u2)
        u2.follow(u3)
        u3.follow(u3)
        u3.follow(u4)
        u4.follow(u4)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()
        #check th followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        assert len(f1) == 3
        assert len(f2) == 2
        assert len(f3) == 2
        assert len(f4) == 1
        assert f1 == [p4, p2, p1]
        assert f2 == [p3, p2]
        assert f3 == [p4, p3]
        assert f4 == [p4]

    def test_delete_post(self):
        #create a user and o post
        u = User(nickname='jo',email='jo@example.com')
        p = Post(body='test eh post', author=u, timestamp=datetime.utcnow())
        db.session.add(u)
        db.session.add(p)
        db.session.commit()
        #querry the post and destroy the session
        p = Post.query.get(1)
        db.session.remove()
        #delete the post using a new session
        db.session = db.create_scoped_session()
        db.session.delete(p)
        db.session.commit()


    def __repr__(self):  #pragma: no cover
        return '<User %r>' %(self.nickname)


#the translate function was cut off.
#    def test_translation(self):
#        assert microsoft_translate(u'English', 'en', 'es') == u'Inglés'
#        assert microsoft_translate(u'Español', 'es', 'en') == u'Spanish'

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()






