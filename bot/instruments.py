""" Refactor data """


def strip_all(value: str):
    """ Strip data """
    return value.lstrip("('").rstrip("',)").strip().replace(' ', '')


def strip_list(value: str):
    """ Strip data """
    return value.lstrip("[('(").rstrip(")',)]").split(',')
