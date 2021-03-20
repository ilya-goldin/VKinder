import unittest
import db
from datetime import datetime as dt


class TestDB(unittest.TestCase):
    def setUp(self):
        self.session = db.Session()

    def test_add_user(self):
        user = db.User(
            user_id=33333333,
            domain='2',
            request_user_id=2,
            first_name='TestFirst',
            last_name='TestLast',
            user_status=True,
            init_data=str(dt.now()),
            offset=0,
            sex=2,
            age=11,
            city=1
        )
        self.session.add(user)
        self.session.commit()
        our_user = self.session.query(db.User).filter_by(user_id=33333333).first()
        self.assertEqual(our_user, user)

    def test_add_match(self):
        user = self.session.query(db.User).filter_by(user_id=33333333).first()
        match = db.Match(
            user_id=22222222,
            domain=123321123,
            first_name="First Name",
            last_name="Last Name",
            user_status=False,
            init_data=str(dt.now()),
            photo=[{"album_id": -6,
                    "date": 1477644876,
                    "id": 22222222,
                    "owner_id": 22222222,
                    "has_tags": False,
                    "post_id": 1,
                    "sizes": {"height": 518,
                              "url": "https://sun9-70.userapi.com/impf/c837436/v837436939/a70b/vEBsqNqI8ns.jpg",
                              "type": "y",
                              "width": 800},
                    "text": "",
                    "likes": {"user_likes": 0,
                              "count": 10},
                    "reposts": {"count": 0},
                    "comments": {"count": 0},
                    "can_comment": 1,
                    "tags": {"count": 0}}],
            match=user
        )
        self.session.add(match)
        self.session.commit()
        our_match = self.session.query(db.Match).filter_by(user_id=22222222).first()
        self.assertEqual(our_match, match)

    def test_match(self):
        self.assertIn(
            self.session.query(db.Match).filter_by(user_id=22222222).first(),
            self.session.query(db.User).filter_by(user_id=33333333).first().match
        )

    def test_delete_match(self):
        cursor = self.session.query(db.Match).filter_by(user_id=22222222).first()
        self.session.delete(cursor)
        self.session.commit()
        self.assertNotIn(
            cursor,
            self.session.query(db.User).filter_by(user_id=33333333).first().match
        )

    def test_delete_user(self):
        cursor = self.session.query(db.User).filter_by(user_id=33333333).first()
        self.session.delete(cursor)
        self.session.commit()
        self.assertNotIn(
            cursor,
            self.session.query(db.User).all()
        )
