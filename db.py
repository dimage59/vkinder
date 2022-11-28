import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

from config import db_user, db_password, db_host, db_port, dbase_name
from models import Base, HunterTable, BlackTable, FavTable, Hunter_Fav, Hunter_Black
from hunter import Hunter

DSN = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{dbase_name}'

engine= sqlalchemy.create_engine(DSN, pool_pre_ping=True)
Session= sessionmaker(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as er:
        session.rollback()
        print(er)
    finally:
        session.close()


async def get_all_hunter_from_db():
    with session_scope() as s:
        results = s.query(HunterTable).all()
        for i in results:
            hunter=Hunter(i.hunter_id,
                          first_name=i.first_name,
                          last_name=i.last_name,
                          search_sex=i.search_sex,
                          search_city_id=i.search_city_id,
                          search_city_title=i.search_city_title,
                          search_age_from=i.search_age_from,
                          search_age_to=i.search_age_to,
                          search_interests=i.search_interests,
                          count_find_users=i.count_find_users
                          )
            Hunter.all_hunters[i.hunter_id]=hunter



async def add_db_hunter(hunter):
    with session_scope() as s:
        new_hunter=HunterTable(hunter_id=hunter.id,
                               first_name=hunter.first_name,
                               last_name=hunter.last_name,
                               search_sex=hunter.search_sex,
                               search_city_id=hunter.search_city_id,
                               search_city_title=hunter.search_city_title,
                               search_age_from=hunter.search_age_from,
                               search_age_to=hunter.search_age_to,
                               search_interests=hunter.search_interests,
                               count_find_users=hunter.count_find_users
                               )
        s.add(new_hunter)


async def get_fav_list(hunter_id):
    fav_list=[]
    with session_scope() as s:
        result= s.query(FavTable).join(Hunter_Fav).join(HunterTable).filter(HunterTable.hunter_id==hunter_id).all()
        for item in result:
            fav_list.append([item.user_id, item.first_name,
                             item.last_name, item.domain,
                             item.bdate, item.main_photo_id])
    return fav_list

async def get_black_list(hunter_id):
    black_list= []
    with session_scope() as s:
        result= s.query(BlackTable).join(Hunter_Black).join(HunterTable).filter(HunterTable.hunter_id==hunter_id).all()
        for item in result:
            black_list.append([item.user_id, item.first_name,
                               item.last_name, item.domain,
                               item.bdate, item.main_photo_id])
    return black_list


#Добавить запись в избранное
async def add_to_fav_list(hunter_id, user):
    with session_scope() as s:
        if not s.query(FavTable).filter(FavTable.user_id==user[0]).first():
            new_user=FavTable(user_id=user[0],
                              first_name=user[1],
                              last_name=user[2],
                              domain=user[3],
                              bdate=user[4],
                              main_photo_id=user[5])
            s.add(new_user)
        if not s.query(Hunter_Fav).filter(Hunter_Fav.user_id==user[0],Hunter_Fav.hunter_id==hunter_id).first():
            new_hunter_fav=Hunter_Fav(hunter_id, user_id=user[0])
            s.add(new_hunter_fav)


#удалить запись из избранного
async def del_from_fav_list(hunter_id,user_id):
        with session_scope() as s:
            del_user=s.query(Hunter_Fav).filter(Hunter_Fav.hunter_id==hunter_id, Hunter_Fav.user_id== user_id).one()
            if del_user:
                s.delete(del_user)
                #если пользователь ни с кем не связан удаляем его из таблицы избранное
                all_notes= s.query(Hunter_Fav).filter(Hunter_Fav.user_id==user_id).all()
                s.delete(del_user)


#добавляем запись в просмотренное
async def add_to_black_list(hunter_id, user):
    with session_scope() as s:
        if not s.query(BlackTable).filter(BlackTable.user_id==user[0]).first():
            new_user = BlackTable(user_id=user[0],
                                  first_name=user[1],
                                  last_name=user[2],
                                  domain=user[3],
                                  bdate=user[4],
                                  main_photo_id=user[5])
            s.add(new_user)
        if not s.query(Hunter_Black).filter(Hunter_Black.user_id==user[0],Hunter_Black.hunter_id==hunter_id).first():
            new_hunter_black= Hunter_Black(hunter_id=hunter_id, user_id=user[0])
            s.add(new_hunter_black)


#удаляем из просмотренное
async def del_from_black_list(hunter_id, user_id):
    with session_scope() as s:
        del_user = s.query(Hunter_Black).filter(Hunter_Black.hunter_id ==hunter_id,Hunter_Black.user_id ==user_id).one()
        if del_user:
            s.delete(del_user)
        all_notes=s.query(Hunter_Black).filter(Hunter_Black.user_id==user_id).all()
        if not all_notes:
            del_user = s.query(BlackTable).filter(BlackTable.user_id==user_id).one()
            s.delete(del_user)

#очищаем избранное
async def clear_all_blacklist(hunter_id):
    with session_scope() as s:
        all_users=s.query(Hunter_Black).filter(Hunter_Black.hunter_id==hunter_id).all()
        for user in all_users:
            await del_from_black_list(hunter_id,user.user_id)


async def change_search_sex(hunter_id, sex):
    with session_scope() as s:
        db_hunter=s.query(HunterTable).filter(HunterTable.hunter_id==hunter_id).one()
        db_hunter.search_status = status


async def change_city(hunter_id, city_id, city_title):
    with session_scope() as s:
        db_hunter=s.query(HunterTable).filter(HunterTable.hunter_id == hunter_id).one()
        db_hunter.search_city_id=city_id
        db_hunter.search_city_title=city_title

async def change_age(hunter_id, age_from, age_to):
    with session_scope() as s:
        db_hunter = s.query(HunterTable).filter(HunterTable.hunter_id == hunter_id).one()
        db_hunter.search_age_from = age_from
        db_hunter.search_age_to = age_to

async def change_interests(hunter_id, interests):
    with session_scope() as s:
        db_hunter = s.query(HunterTable).filter(HunterTable.hunter_id == hunter_id).one()
        db_hunter.search_interests = interests

async def recreate_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



