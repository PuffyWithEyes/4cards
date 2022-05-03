""" States of classes """
from aiogram.dispatcher.filters.state import State, StatesGroup


class DoReport(StatesGroup):
    r = State()


class ReportShareVK(StatesGroup):
    s = State()
    message = State()


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


class Test(StatesGroup):
    t = State()
