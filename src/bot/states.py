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


class YesNoDict(StatesGroup):
    y = State()


class NoDict(StatesGroup):
    n = State()


class CreateApassword(StatesGroup):
    c = State()


class Apanel(StatesGroup):
    a = State()


class EnterAdmin(StatesGroup):
    e = State()


class SetAdminPassword(StatesGroup):
    s = State()


class Sudo(StatesGroup):
    s = State()


class AcceptAdd(StatesGroup):
    a = State()


class NotDo(StatesGroup):
    n = State()


class ProofNo(StatesGroup):
    p = State()


class FindUsers(StatesGroup):
    f = State()


class FindShareVK(StatesGroup):
    f = State()


class FindIDTG(StatesGroup):
    f = State()


class FindCardNumber(StatesGroup):
    f = State()


class FindTelephoneNumber(StatesGroup):
    f = State()


class FindAddress(StatesGroup):
    f = State()


class YesNoAddress(StatesGroup):
    y = State()


class NoAddress(StatesGroup):
    n = State()


class AddDocsDelete(StatesGroup):
    a = State()


class AcceptDelete(StatesGroup):
    a = State()


class Continue(StatesGroup):
    c = State()
