""" Refactor data """
from con_db.actions_db import UpdateInfo, FindUser
from aiogram import types


def strip_all(value: str):
    """ Strip data """
    return value.lstrip("('").rstrip("',)").strip().replace(' ', '')


def strip_list(value: str):
    """ Strip data """
    return value.lstrip("[('(").rstrip(")',)]").split(',')


def strip_alist(value: str):
    """ Strip data """
    return value.lstrip("[(").rstrip(",)]").replace('(', '').replace(')', '').replace(',', '').split(',')


def strip_report(value: str):
    """ Strip data """
    return value.lstrip("[(").rstrip(",)]").replace('(', '').replace(')', '').replace(',', '').split(' ')


def strip_default_list(value: str):
    """ Strip data """
    return str(value).rstrip('''']"''').lstrip(""""['""")


def check_place(value_list: list, data: str):
    """ Function for check place of admin """
    data = strip_default_list(data)
    return int(sorted(set(value_list)).index(str(data))) + 1


def strip_parentheses(value: str):
    """ Function for strip parentheses """
    return value.lstrip('(').rstrip(')').split(', ')


def s_none(value):
    """ Function for check none """
    if str(value).lower() != 'none':
        return "'" + str(value) + "'"
    elif str(value).isdigit():
        return int(value)
    else:
        return 'Null'


def c_none(value):
    """ Function for check none """
    if str(value).lower() == 'none':
        return 'Отсутствует'
    else:
        return value.replace("'", '')


async def social_rating(message: types.Message):
    """ Update social rating of admins """
    credit = int(strip_all(str(connect.find_matches_where_one(find_column='social_credit', table='admin_panel',
                                                              where_column='user_id', data=int(message.from_user.id),
                                                              flag=True))))
    update.update_where(table='admin_panel', table_what='social_credit', data_what=(credit + 1), table_where='user_id',
                        data_where=int(message.from_user.id))


connect = FindUser()
update = UpdateInfo()
