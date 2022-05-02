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


class YesNo(StatesGroup):
    y = State()


class No(StatesGroup):
    n = State()
    temp = State()


class Data(StatesGroup):
    d = State()
