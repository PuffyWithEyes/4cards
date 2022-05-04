""" States of classes """
from aiogram.dispatcher.filters.state import State, StatesGroup


class DoReport(StatesGroup):
    r = State()


class ReportShareVK(StatesGroup):
    s = State()


class ReportIDTG(StatesGroup):
    i = State()


class CardNumber(StatesGroup):
    c = State()


class TelephoneNumber(StatesGroup):
    t = State()


class Address(StatesGroup):
    a = State()


class ID(StatesGroup):
    i = State()


class YesNoVK(StatesGroup):
    y = State()


class NoVK(StatesGroup):
    n = State()


class YesNoTG(StatesGroup):
    y = State()


class NoTG(StatesGroup):
    n = State()


class YesNoCard(StatesGroup):
    y = State()


class NoCard(StatesGroup):
    n = State()


class YesNoTelephone(StatesGroup):
    y = State()


class NoTelephone(StatesGroup):
    n = State()


class DocsCard(StatesGroup):
    d = State()
