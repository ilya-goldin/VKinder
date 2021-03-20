import db
import vkuser
import chatbot
from datetime import datetime as dt
from json import dump


def get_data(usr, request_user_id):
    if isinstance(usr.user_status, bool):
        pass
    elif isinstance(usr.user_status[0], list):
        x = chatbot.ChatBot()
        if 'bdate' in usr.user_status[0]:
            usr.age = int(x.requests_data('bdate', request_user_id))
        if 'city' in usr.user_status[0]:
            usr.city = usr.get_city(x.requests_data('city', request_user_id))
        if 'sex' in usr.user_status[0]:
            user_sex = int(x.requests_data('sex', request_user_id))
            usr.sex = 2 if (user_sex == 1) else 1
        usr.user_status = usr.user_status[1]


def db_insert_user(usr, sess, req_id):
    insert = db.User(user_id=usr.user_id,
                     domain=usr.domain,
                     request_user_id=req_id,
                     first_name=usr.first_name,
                     last_name=usr.last_name,
                     user_status=usr.user_status,
                     init_data=str(dt.now()),
                     offset=usr.offset,
                     sex=usr.sex,
                     age=usr.age,
                     city=usr.city)
    sess.add(insert)
    sess.commit()
    return insert


def db_insert_match(usr, sess, match, photo):
    insert = db.Match(user_id=match['id'],
                      domain=match['domain'],
                      first_name=match['first_name'],
                      last_name=match['last_name'],
                      user_status=match['is_closed'],
                      init_data=str(dt.now()),
                      photo=photo,
                      match=usr)
    sess.add(insert)
    sess.commit()


def main():
    x = chatbot.ChatBot()
    get = x.search()
    if get:
        session = db.Session()
        if isinstance(get[0], int):
            db_user = session.query(db.User).filter_by(user_id=get[0]).first()
        else:
            db_user = session.query(db.User).filter_by(domain=get[0]).first()
        if not db_user:
            user = vkuser.VKUser(get[0], get[1], 0)
            get_data(user, get[1])
            db_user = db_insert_user(user, session, get[1])
        else:
            user = vkuser.VKUser(db_user.user_id,
                                 db_user.request_user_id,
                                 db_user.offset,
                                 new_user=False)
            user.domain = db_user.domain
            user.first_name = db_user.first_name
            user.last_name = db_user.last_name
            user.user_status = db_user.user_status
            user.sex = db_user.sex
            user.age = db_user.age
            user.city = db_user.city
        result = []
        while len(result) < 10:
            response = user.__next__()
            if response is None:
                continue
            elif len(response) == 0:
                continue
            for item in response:
                check = session.query(db.Match).filter_by(match_id=db_user.id).filter_by(user_id=item['id']).first()
                if check:
                    continue
                elif item['is_closed']:
                    continue
                photo = user.get_profile_photos(item['id'])
                result.append(('https://vk.com/' + item['domain'], photo))
                db_insert_match(db_user, session, item, photo)
        db_user.offset = user.offset
        session.add(db_user)
        session.commit()
        for i in result:
            photos = [photo['sizes']['url'] for photo in i[1]]
            x.attach_image(db_user.request_user_id, photos, i[0])
        with open('result.json', 'w') as outfile:
            dump(result, outfile)


if __name__ == '__main__':
    main()
