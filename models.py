import sqlalchemy as sq
from sqlalchemy.orm import declarative_base,relationship

Base=declarative_base()

class Hunter_Fav(Base):
    __tablename__: str='Hunter_Fav'
    id = sq.Column(sq.Numeric, primary_key=True)
    hunter_id=sq.Column(sq.BIGINT,sq.ForeignKey('huntertable.hunter_id'))
    user_id= sq.Column(sq.BIGINT,sq.ForeignKey('favtable.user_id'))

class Hunter_Black(Base):
    __tablename__: str= 'Hunter_Black'
    id= sq.Column(sq.Numeric, primary_key=True)
    hunter_id=sq.Column(sq.BIGINT,sq.ForeignKey('huntertable.hunter_id'))
    user_id = sq.Column(sq.BIGINT,sq.ForeignKey('blacktable.user_id'))
class HunterTable(Base):
    __tablename__: str='HunterTable'
    id = sq.Column(sq.Numeric, primary_key= True)
    hunter_id = sq.Column(sq.BIGINT, unique=True)
    first_name = sq.Column(sq.String(50))
    last_name = sq.Column(sq.String(50))
    search_sex = sq.Column(sq.Integer)
    search_city_id = sq.Column(sq.Integer)
    search_city_title = sq.Column(sq.String(100))
    search_age_from = sq.Column(sq.Integer)
    search_age_to = sq.Column(sq.Integer)
    search_interests = sq.Column(sq.Text)
    search_status = sq.Column(sq.Integer)
    count_find_users = sq.Column(sq.Integer)
    favtable = relationship('Hunter_Fav', backref='HunterTable')
    blacktable = relationship('Hunter_Black', backref='HunterTable')

class FavTable(Base):
    __tablename__: str= 'FavTable'
    id = sq.Column(sq.Numeric, primary_key=True)
    user_id = sq.Column(sq.BIGINT, unique=True)
    first_name = sq.Column(sq.String(50))
    last_name = sq.Column(sq.String(50))
    domain = sq.Column(sq.String(50))
    bdate = sq.Column(sq.String(50))
    main_photo_id = sq.Column(sq.String(50))
    huntertable = relationship('Hunter_Fav', backref='FavTable')


class BlackTable(Base):
    __tablename__:str = 'BlackTable'
    id = sq.Column(sq.Numeric, primary_key=True)
    user_id = sq.Column(sq.BIGINT, unique=True)
    first_name = sq.Column(sq.String(50))
    last_name = sq.Column(sq.String(50))
    domain = sq.Column(sq.String(50))
    bdate = sq.Column(sq.String(50))
    main_photo_id = sq.Column(sq.String(50))
    huntertable = relationship('Hunter_Black', backref='BlackTable')


def create_tables( engine ):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

