from sqlalchemy.sql import func
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import select, update, create_engine, Column, String, Integer, BigInteger, DateTime, Boolean, \
    TIMESTAMP, Date

from config import DATABASE

DeclarativeBase = declarative_base()
engine = create_engine(URL.create(**DATABASE), echo=False)
session = Session(engine)


class Config(DeclarativeBase):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group = Column(String)
    token = Column(String)
    expired_date = Column(DateTime)
    comment = Column(String)
    date = Column(TIMESTAMP, server_default=func.now())
    last_update = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.current_timestamp())


class Users(DeclarativeBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    is_admin = Column(Boolean)
    is_blocked = Column(Boolean)
    total_audio = Column(Integer)
    birth_date = Column(Date)
    date = Column(TIMESTAMP, server_default=func.now())
    last_update = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.current_timestamp())


class Groups(DeclarativeBase):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_id = Column(BigInteger)
    group_title = Column(String)
    total_users = Column(Integer)
    date = Column(TIMESTAMP, server_default=func.now())
    last_update = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.current_timestamp())


class UserGroups(DeclarativeBase):
    __tablename__ = 'user_groups'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    is_left = Column(Boolean)
    group_id = Column(BigInteger)
    date = Column(TIMESTAMP, server_default=func.now())
    last_update = Column(TIMESTAMP, server_default=func.now(), server_onupdate=func.current_timestamp())


class Disk(DeclarativeBase):
    __tablename__ = 'disk'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    file_name = Column(String)
    file_link = Column(String)
    file_password = Column(String)
    comment = Column(String)
    delete_days = Column(Integer)
    is_deleted = Column(Boolean)
    date = Column(TIMESTAMP, server_default=func.now())


class Logs(DeclarativeBase):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    message_id = Column(BigInteger)
    user_id = Column(BigInteger)
    lang = Column(String)
    group_id = Column(BigInteger)
    group_type = Column(String)
    message_text = Column(String)
    message_type = Column(String)
    date = Column(TIMESTAMP, server_default=func.now())


class Vpn(DeclarativeBase):
    __tablename__ = 'vpn'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    vpn_login = Column(String)
    vpn_setup = Column(String)
    is_blocked = Column(Boolean)
    comment = Column(String)
    date = Column(TIMESTAMP, server_default=func.now())
    last_update = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())


def users_insert(message):  # Запись в таблицу Users
    line = Users(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        is_admin=False,
        is_blocked=False
    )
    session.add(line)
    session.commit()


def users_update(message):  # Обновление в таблице Users
    session.execute(update(Users)
                    .where(Users.user_id == message.from_user.id)
                    .values(first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username))
    session.commit()


def groups_insert(message):  # Запись в таблицу Groups
    line = Groups(
        group_id=message.chat.id,
        group_title=message.chat.title
    )
    session.add(line)
    session.commit()


def groups_update(message):  # Обновление в таблице Groups
    total_users = session.query(UserGroups.group_id) \
        .filter(UserGroups.group_id == message.chat.id).filter(UserGroups.is_left == False).count()
    session.execute(update(Groups)
                    .where(Groups.group_id == message.chat.id)
                    .values(group_title=message.chat.title,
                            total_users=total_users))
    session.commit()


def user_groups_insert(message):  # Запись в таблицу UserGroups
    line = UserGroups(
        user_id=message.from_user.id,
        is_left=False,
        group_id=message.chat.id
    )
    session.add(line)
    session.commit()


def user_groups_update(message):  # Обновление в таблице UserGroups
    session.execute(update(UserGroups)
                    .where(UserGroups.user_id == message.from_user.id and
                           UserGroups.group_id == message.chat.id)
                    .values(is_left=False))
    session.commit()


def disk_insert(message, file_name, file_link, file_password, delete_days=10):  # Запись в таблицу Disk
    line = Disk(
        user_id=message.from_user.id,
        file_name=file_name,
        file_link=file_link,
        file_password=file_password,
        delete_days=delete_days,
        is_deleted=False
    )
    session.add(line)
    session.commit()


def log_insert(message):  # Запись в таблицу Logs
    line = Logs(
        message_id=message.message_id,
        user_id=message.from_user.id,
        lang=message.json['from']['language_code'],
        group_id=message.json['chat']['id'],
        group_type=message.json['chat']['type'],
        message_text=message.json['text'],
        message_type=message.content_type
    )
    session.add(line)
    session.commit()


def vpn_insert(message, host='fb-fin'):  # Запись в таблицу Vpn
    if message.from_user.username is None:  # fb-us, fb-fin, fb-ru, fb-sin | iOS/Mac, Android, Windows
        vpn_login = message.from_user.id
    else:
        vpn_login = message.from_user.username
    line = Vpn(
        user_id=message.from_user.id,
        vpn_login=vpn_login,
        vpn_setup=f'{host} | iOS/Mac, Android',
        is_blocked=False
    )
    session.add(line)
    session.commit()


def auto_clean_disk_files(YandexDisk, YA_DISK_TOKEN):
    for file_name in session.scalars(select(Disk.file_name).where(Disk.is_deleted == False)).all():
        delete_days = session.scalars(select(Disk.delete_days).where(Disk.file_name == file_name)).first()
        if delete_days == 0:
            YandexDisk(YA_DISK_TOKEN).delete_file(file_name)
            session.execute(update(Disk).where(Disk.file_name == file_name).values(is_deleted=True))
            session.commit()
        else:
            session.execute(update(Disk).where(Disk.file_name == file_name).values(delete_days=(delete_days - 1)))
            session.commit()


def work_with_db(message):  # Основная функция которая делает записи в DB
    DeclarativeBase.metadata.create_all(engine)  # Создаёт все таблицы
    if message.from_user.is_bot is False:
        # Взаимодействие с таблицей Users
        if session.scalars(select(Users.user_id).where(Users.user_id == message.from_user.id)).first() is None:
            users_insert(message)  # Запись новой строки
        users_update(message)  # Обновление существующей строки
        if message.chat.type != 'private':
            # Взаимодействие с таблицей UserGroups
            if session.scalars(select(UserGroups).where(UserGroups.user_id == message.from_user.id and
                                                        UserGroups.group_id == message.chat.id)).first() is None:
                user_groups_insert(message)  # Запись новой строки
            user_groups_update(message)  # Обновление существующей строки
            # Взаимодействие с таблицей Groups
            if session.scalars(select(Groups.group_id).where(Groups.group_id == message.chat.id)).first() is None:
                groups_insert(message)  # Запись новой строки
            groups_update(message)  # Обновление существующей строки


def get_token(name, group):
    return session.scalars(select(Config.token).where(Config.name == name and Config.group == group)).first()


def get_groups():
    groups = []
    for line in session.query(Groups.group_id, Groups.group_title).all():
        groups.append(line)
    return ''.join(str(groups))


def get_total_audio(message):
    if session.scalars(select(Users.total_audio).where(Users.user_id == message.from_user.id)).first() is None:
        update_total_audio(message, audio_time=300)
    return session.scalars(select(Users.total_audio).where(Users.user_id == message.from_user.id)).first()


def update_total_audio(message, audio_time):
    session.execute(update(Users).where(Users.user_id == message.from_user.id)
                    .values(total_audio=audio_time))
    session.commit()


def update_is_left(message, is_left):
    if is_left is True:
        session.execute(update(UserGroups)
                        .where(UserGroups.user_id == message.left_chat_member.id and
                               UserGroups.group_id == message.chat.id)
                        .values(is_left=is_left))
    else:
        session.execute(update(UserGroups)
                        .where(UserGroups.user_id == message.new_chat_members[0].id and
                               UserGroups.group_id == message.chat.id)
                        .values(is_left=is_left))
    session.commit()


def get_cell(message, bool_param):
    where_column = Users.user_id
    if bool_param == 'is_admin':
        bool_param = Users.is_admin
    elif bool_param == 'is_blocked':
        bool_param = Users.is_blocked
    elif bool_param == 'get_balance':
        bool_param = Users.total_audio
    elif bool_param == 'is_vpn_blocked':
        bool_param = Vpn.is_blocked
        where_column = Vpn.user_id
    elif bool_param == 'get_vpn_login':
        bool_param = Vpn.vpn_login
        where_column = Vpn.user_id
    elif bool_param == 'get_vpn_setup':
        bool_param = Vpn.vpn_setup
        where_column = Vpn.user_id
    return session.scalars(select(bool_param).where(where_column == message.from_user.id)).first()


def is_vpn_user_exist(message):
    if session.scalars(select(Vpn.user_id).where(Vpn.user_id == message.from_user.id)).first() is None:
        return False
    else:
        return True
