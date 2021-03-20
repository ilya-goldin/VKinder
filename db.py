import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from config import DSN

Base = declarative_base()
engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, sq.Sequence('user_id_seq'), primary_key=True)
    match = relationship('Match', backref='match')

    user_id = sq.Column(sq.Integer, unique=True)
    domain = sq.Column(sq.String(30), unique=True)
    request_user_id = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String(30))
    last_name = sq.Column(sq.String(80))
    user_status = sq.Column(sq.Boolean)
    init_data = sq.Column(sq.Date)
    offset = sq.Column(sq.Integer)

    sex = sq.Column(sq.Integer)
    age = sq.Column(sq.Integer)
    city = sq.Column(sq.Integer)

    def __repr__(self):
        return f'https://vk.com/{self.domain}'


class Match(Base):
    __tablename__ = 'match'
    id = sq.Column(sq.Integer, primary_key=True)
    match_id = sq.Column(sq.Integer, sq.ForeignKey('user.id'))

    user_id = sq.Column(sq.Integer, nullable=False)
    domain = sq.Column(sq.String(30))
    first_name = sq.Column(sq.String(30))
    last_name = sq.Column(sq.String(80))
    user_status = sq.Column(sq.Boolean)
    init_data = sq.Column(sq.Date)
    photo = sq.Column(sq.JSON)

    def __repr__(self):
        return f'https://vk.com/{self.domain}'


if __name__ == '__main__':
    Base.metadata.create_all(engine)
