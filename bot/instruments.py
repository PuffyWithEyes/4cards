""" Refactor data """


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
