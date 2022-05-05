from con_db.actions_db import FindUser


def strip_all(value: str):
    return value.lstrip("('").rstrip("',)").strip()


def strip_json(value: str):
    return value.lstrip("('").rstrip("',)").strip().replace('"', '').replace(',', '').split()


def plus_json(message):
    data = find.find_matches_where_two(data=int(message.from_user.id), find_column_one='key', find_column_two='value',
                                       table='json', where_column='user_id')
    data_list_1 = []
    data_list_2 = []
    for i in data:
        i = strip_json(str(i))
        data_list_1.append(("'" + i[0] + "'"))
        data_list_2.append(i[1].lower())

    data_dict = dict(zip(data_list_1, data_list_2))
    del data_list_1, data_list_2, data
    return data_dict


find = FindUser()
