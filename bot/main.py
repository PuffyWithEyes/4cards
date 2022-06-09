# Script for python version 3.9 and for Debian Linux
from aiogram import Bot, Dispatcher, executor, types
from bot.config import TOKEN, RED_ADMIN, RED_ADMIN_PASSWORD
from aiogram.dispatcher.filters import Text
import data.markup as nav
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from con_db.actions_db import FindUser, AddUser, DeleteInfo, UpdateInfo
import states
import data.text as txt
from instruments import strip_all, strip_list, check_place, strip_alist, strip_report
from con_db.ClearMessages import ClearMessages
from con_db.Create import Create
from bot.instruments import strip_parentheses


# Global settings for the bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands='start')
async def start(message: types.Message):
    """ Function of start """
    await message.answer(txt.START_TEXT, reply_markup=nav.main_menu)


@dp.message_handler(Text(equals='ℹИнформация'))
async def info(message: types.Message):
    """ Function of information """
    await message.answer(txt.INFO_TEXT, reply_markup=nav.info_menu)


@dp.message_handler(Text(equals='📝Подать жалобу'))
async def do_report(message: types.Message):
    """ Function of report """
    await message.answer(txt.REPORT_TEXT, reply_markup=nav.selections_menu)


@dp.message_handler(Text(equals='🔭Найти пользователя'))
async def find_user(message: types.Message):
    """ Function of search of information about user """
    await message.answer(txt.FIND_TEXT)


@dp.message_handler(Text(equals='➕Подать жалобу на внесение в ЧС'))
async def add_user(message: types.Message):
    """ Function for add user in black list """
    await states.DoReport.r.set()
    await message.answer(txt.ADD_TEXT, reply_markup=nav.report_menu)


@dp.message_handler(Text(equals='➖Подать жалобу на удаление из ЧС'))
async def delete_user(message: types.Message):
    """ Function for delete user from black list """
    await message.answer(txt.DELETE_TEXT)


@dp.message_handler(state=states.DoReport.r)
async def do_report(message: types.Message, state: FSMContext):
    """ Function of report """
    r = message.text
    if r == '⛓Проверить ссылку во ВКонтакте':
        await state.finish()
        await states.ReportShareVK.s.set()
        await message.reply(txt.VK_TEXT, reply_markup=nav.cancel_menu)

    elif r == '🆔Проверить по ID в Telegram':
        await state.finish()
        await states.ReportIDTG.i.set()
        await message.reply(txt.TG_TEXT, reply_markup=nav.cancel_menu)

    elif r == '💳Проверить по номеру карты':
        await state.finish()
        await states.CardNumber.c.set()
        await message.reply(txt.CARD_TEXT, reply_markup=nav.cancel_menu)

    elif r == '📞Проверить по номеру телефона':
        await state.finish()
        await states.TelephoneNumber.t.set()
        await message.reply(txt.TELEPHONE_TEXT, reply_markup=nav.cancel_menu)

    elif r == '🏠Проверить по адресу':
        await state.finish()
        await states.Address.a.set()
        await message.reply(txt.ADDRESS_TEXT, reply_markup=nav.cancel_menu)

    elif r == '🧾У меня есть ID мошенника из базы данных':
        await state.finish()
        await states.ID.i.set()
        await message.reply(txt.ID_TEXT, reply_markup=nav.cancel_menu)

    elif r == '🔄Вернуться назад':
        await state.finish()
        await state.reset_state()
        await message.answer(txt.BACK_TEXT, reply_markup=nav.selections_menu)

    else:
        await message.reply(txt.ELSE_TEXT)


@dp.message_handler(state=states.ReportShareVK.s)
async def check_vk(message: types.Message, state: FSMContext):
    """ Function for check matches """
    s = message.text
    if s == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)
        
    elif s == '🔄Вернуться назад':
        await state.finish()
        await message.answer(txt.BACK_TEXT, reply_markup=nav.selections_menu)
        
    elif 15 < len(s) < 129 and (s[0:17] == txt.VK_CM or s[0:16] == txt.VK_CMN or s[0:15] == txt.VK_C or s[0:14] ==
                                txt.VK_CN) and s.find("'") < 0 and s.find(' ') < 0:
        matches = connect.find_matches(mean=s, column='share_vk')

        if matches[0]:
            await state.finish()
            await states.YesNoVK.y.set()
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}', reply_markup=nav.selections_menu)
        else:
            await state.finish()
            await states.YesNoVK.y.set()
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=s, first_column='user_id',
                        second_column='message', table='messages')
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.YesNoVK.y)
async def ask_info_vk(message: types.Message, state: FSMContext):
    """ Function for ask user about info """
    y = message.text
    if y == '👍Да':
        await state.finish()
        await states.DoReport.r.set()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.YES_TEXT, reply_markup=nav.report_menu)

    elif y == '👎Нет':
        await state.finish()
        await states.NoVK.n.set()
        await message.answer(txt.DOC_TEXT, reply_markup=nav.o_cancel_menu)

    elif y == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.NoVK.n)
async def add_docs_vk(message: types.Message, state: FSMContext):
    """ This function add proofs in database """
    n = message.text
    if n == '❌Отменить действие':
        await state.finish()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)

    elif 22 < len(n) < 256 and (n[0:24] == txt.YOUTUBE_C or n[0:23] == txt.YOUTUBE_CN or n[0:22] == txt.YOUTUBE_CM or
                                n[0:21] == txt.YOUTUBE_CMN or n[0:17] == txt.YOUTUBE_BEC or n[0:16] == txt.YOUTUBE_BECN
                                or n[0:19] == txt.YOUTUBE_BEMC or n[0:18] == txt.YOUTUBE_BEMCN) and n.find("'") < 0 \
            and n.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id')))
        add.add_two(first_value=n, second_value=data, first_column='docers',
                    second_column='share_vk', table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.ReportIDTG.i)
async def check_tg(message: types.Message, state: FSMContext):
    """ Function for check matches """
    i = message.text
    if i == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    elif i == '🔄Вернуться назад':
        await state.finish()
        await message.answer(txt.BACK_TEXT, reply_markup=nav.selections_menu)

    elif len(i) < 65 and i.find("'") < 0 and i.find(' ') < 0:
        matches = connect.find_matches(mean=i, column='share_tg')

        if matches[0]:
            await state.finish()
            await states.YesNoTG.y.set()
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}', reply_markup=nav.selections_menu)
        else:
            await state.finish()
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=i, first_column='user_id',
                        second_column='message', table='messages')
            await states.YesNoTG.y.set()
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.YesNoTG.y)
async def add_info_tg(message: types.Message, state: FSMContext):
    """ Function for ask user about info """
    y = message.text
    if y == '👍Да':
        await state.finish()
        await states.DoReport.r.set()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.YES_TEXT, reply_markup=nav.report_menu)

    elif y == '👎Нет':
        await state.finish()
        await states.NoTG.n.set()
        await message.answer(txt.DOC_TEXT, reply_markup=nav.o_cancel_menu)

    elif y == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.NoTG.n)
async def add_docs_tg(message: types.Message, state: FSMContext):
    """ This function add proofs in database """
    n = message.text
    if n == '❌Отменить действие':
        await state.finish()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)

    elif 22 < len(n) < 256 and (n[0:24] == txt.YOUTUBE_C or n[0:23] == txt.YOUTUBE_CN or n[0:22] == txt.YOUTUBE_CM or
                                n[0:21] == txt.YOUTUBE_CMN or n[0:17] == txt.YOUTUBE_BEC or n[0:16] == txt.YOUTUBE_BECN
                                or n[0:19] == txt.YOUTUBE_BEMC or n[0:18] == txt.YOUTUBE_BEMCN) and n.find("'") < 0\
            and n.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id')))
        add.add_two(first_value=n, second_value=data, first_column='docers',
                    second_column='share_tg', table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.CardNumber.c)
async def check_card(message: types.Message, state: FSMContext):
    """ Function for check matches """
    c = message.text
    if c == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    elif c == '🔄Вернуться назад':
        await state.finish()
        await message.answer(txt.BACK_TEXT, reply_markup=nav.selections_menu)

    elif len(c) == 16 and isinstance(int(c), int):
        matches = connect.find_matches(mean=int(c), column='cnumber')

        if matches[0]:
            await state.finish()
            await states.YesNoCard.y.set()
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}', reply_markup=nav.selections_menu)
        else:
            await state.finish()
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=int(c), first_column='user_id',
                        second_column='message', table='messages')
            await states.YesNoCard.y.set()
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.YesNoCard.y)
async def add_info_card(message: types.Message, state: FSMContext):
    """ Function for ask user about info """
    y = message.text
    if y == '👍Да':
        await state.finish()
        await states.DoReport.r.set()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.YES_TEXT, reply_markup=nav.report_menu)

    elif y == '👎Нет':
        await state.finish()
        await states.NoCard.n.set()
        await message.answer(txt.DOC_TEXT, reply_markup=nav.o_cancel_menu)

    elif y == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.NoCard.n)
async def add_docs_card(message: types.Message, state: FSMContext):
    """ This function add proofs in database """
    n = message.text
    if n == '❌Отменить действие':
        await state.finish()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)

    elif 22 < len(n) < 256 and (n[0:24] == txt.YOUTUBE_C or n[0:23] == txt.YOUTUBE_CN or n[0:22] == txt.YOUTUBE_CM or
                                n[0:21] == txt.YOUTUBE_CMN or n[0:17] == txt.YOUTUBE_BEC or n[0:16] == txt.YOUTUBE_BECN
                                or n[0:19] == txt.YOUTUBE_BEMC or n[0:18] == txt.YOUTUBE_BEMCN) and n.find("'") < 0 \
            and n.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id')))
        add.add_two(first_value=n, second_value=int(data), first_column='docers', second_column='cnumber',
                    table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.TelephoneNumber.t)
async def check_telephone(message: types.Message, state: FSMContext):
    """ Function for check matches """
    t = message.text
    if t == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    elif t == '🔄Вернуться назад':
        await state.finish()
        await message.answer(txt.BACK_TEXT, reply_markup=nav.selections_menu)

    elif len(t) < 17 and t.find("'") < 0 and t[0] == '+' and t.find(' ') < 0:
        matches = connect.find_matches(mean=t, column='tnumber')

        if matches[0]:
            await state.finish()
            await states.YesNoTelephone.y.set()
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}', reply_markup=nav.selections_menu)
        else:
            await state.finish()
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=t, first_column='user_id',
                        second_column='message', table='messages')
            await states.YesNoTelephone.y.set()
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.YesNoTelephone.y)
async def add_info_telephone(message: types.Message, state: FSMContext):
    """ Function for ask user about info """
    y = message.text
    if y == '👍Да':
        await state.finish()
        await states.DoReport.r.set()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.YES_TEXT, reply_markup=nav.report_menu)

    elif y == '👎Нет':
        await state.finish()
        await states.NoTelephone.n.set()
        await message.answer(txt.DOC_TEXT, reply_markup=nav.o_cancel_menu)

    elif y == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.NoTelephone.n)
async def add_docs_telephone(message: types.Message, state: FSMContext):
    """ This function add proofs in database """
    n = message.text
    if n == '❌Отменить действие':
        await state.finish()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)

    elif 22 < len(n) < 256 and (n[0:24] == txt.YOUTUBE_C or n[0:23] == txt.YOUTUBE_CN or n[0:22] == txt.YOUTUBE_CM or
                                n[0:21] == txt.YOUTUBE_CMN or n[0:17] == txt.YOUTUBE_BEC or n[0:16] == txt.YOUTUBE_BECN
                                or n[0:19] == txt.YOUTUBE_BEMC or n[0:18] == txt.YOUTUBE_BEMCN) and n.find("'") < 0 \
            and n.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id')))
        add.add_two(first_value=n, second_value=data, first_column='docers',
                    second_column='tnumber', table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.ID.i)
async def ask_id(message: types.Message, state: FSMContext):
    """ This function ask user about swindler's ID """
    i = message.text
    if i == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    elif i == '🔄Вернуться назад':
        await state.finish()
        await message.answer(txt.BACK_TEXT, reply_markup=nav.selections_menu)

    elif isinstance(int(i), int):
        if connect.find_matches_where_one(data=int(i), find_column='id', table='cards_true', where_column='id'):
            await state.finish()
            await message.answer(txt.DOC_TEXT, reply_markup=nav.o_cancel_menu)
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=int(i), first_column='user_id',
                        second_column='message', table='messages')
            await states.DocsCard.d.set()
        else:
            await message.reply(txt.NO_ID, reply_markup=nav.o_cancel_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.DocsCard.d)
async def add_docs_card(message: types.Message, state: FSMContext):
    """ This function add proofs in database """
    d = message.text
    if d == '❌Отменить действие':
        await state.finish()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)

    elif 22 < len(d) < 256 and (d[0:24] == txt.YOUTUBE_C or d[0:23] == txt.YOUTUBE_CN or d[0:22] == txt.YOUTUBE_CM or
                                d[0:21] == txt.YOUTUBE_CMN or d[0:17] == txt.YOUTUBE_BEC or d[0:16] == txt.YOUTUBE_BECN
                                or d[0:19] == txt.YOUTUBE_BEMC or d[0:18] == txt.YOUTUBE_BEMCN) and d.find("'") < 0 \
            and d.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id')))
        add.add_two(first_value=d, second_value=int(data), first_column='docers',
                    second_column='got_id', table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


# @dp.message_handler(state=states.Address.a)
# async def check_address(message: types.Message, state: FSMContext):
#     """ This function ask user swindler's house """
#     a = message.text
#     if a == '❌Отменить действие':
#         await state.finish()
#         await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)
#
#     elif a == '🔄Вернуться назад':
#         await state.finish()
#         await message.answer(txt.BACK_TEXT, reply_markup=nav.selections_menu)
#
#     elif len(a) < 65 and a.find("'") < 0 and a.count(',') == 4:
#         matches = connect.find_matches(mean=a, column='address')
#         if matches[0]:
#             await state.finish()
#             await states.YesNoDict.y.set()
#             await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
#                                 f'{txt.USER_FIND_TEXT_P2}', reply_markup=nav.selections_menu)
#         else:
#             await state.finish()
#             delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
#             add.add_two(first_value=int(message.from_user.id), second_value=a, first_column='user_id',
#                         second_column='message', table='messages')
#             await states.YesNoDict.y.set()
#             await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)
#
#     else:
#         await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)
#
#
# @dp.message_handler(state=states.YesNoDict.y)
# async def add_info_address(message: types.Message, state: FSMContext):
#     """ Function for ask user about info """
#     y = message.text
#     if y == '👍Да':
#         await state.finish()
#         await states.DoReport.r.set()
#         await message.answer(txt.YES_TEXT, reply_markup=nav.report_menu)
#
#     elif y == '👎Нет':
#         await state.finish()
#         await states.NoTelephone.n.set()
#         await message.answer(txt.DOC_TEXT, reply_markup=nav.o_cancel_menu)
#
#     elif y == '❌Отменить действие':
#         await state.finish()
#         await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)
#
#     else:
#         await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)
#
#
# @dp.message_handler(state=states.NoDict.n)
# async def add_docs_address(message: types.Message, state: FSMContext):
#     """ This function add proofs in database """
#     n = message.text
#     if n == '❌Отменить действие':
#         await state.finish()
#         await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)
#
#     elif 22 < len(n) < 256 and (n[0:24] == txt.YOUTUBE_C or n[0:23] == txt.YOUTUBE_CN or n[0:22] == txt.YOUTUBE_CM or
#                                 n[0:21] == txt.YOUTUBE_CMN or n[0:17] == txt.YOUTUBE_BEC or n[0:16] == txt.YOUTUBE_BECN
#                                 or n[0:19] == txt.YOUTUBE_BEMC or n[0:18] == txt.YOUTUBE_BEMCN) and n.find("'") < 0:
#         await state.finish()
#         add.add_two(first_value=n, second_value=plus_dict(message), first_column='docers',
#                     second_column='address', table='cards_report')
#         await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)
#
#     else:
#         await message.reply(txt.WRONG_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(commands='ahelp')
async def a_help(message: types.Message):
    """ Function of admins' help """
    if connect.find_matches_where_one(data=int(message.from_user.id), find_column='user_id', table='admin_panel',
                                      where_column='user_id'):
        await message.answer(txt.ADMIN_HELP_TEXT, reply_markup=nav.main_menu)
    else:
        await message.answer(txt.ACCESS_TEXT, reply_markup=nav.main_menu)


@dp.message_handler(commands='sudo')
async def set_admin(message: types.Message):
    """ Function for set admins in database """
    if int(message.from_user.id) == int(RED_ADMIN):
        await states.SetAdminPassword.s.set()
        await message.answer(txt.SUDO_TEXT)
    else:
        await message.answer(txt.ACCESS_TEXT)


@dp.message_handler(state=states.SetAdminPassword.s)
async def enter_admin_password(message: types.Message, state: FSMContext):
    """ Function for sudo admin """
    s = message.text
    if int(s) == int(RED_ADMIN_PASSWORD):
        await states.SetAdmin.s.set()
        await message.answer(txt.SET_ADMIN_TEXT)
    else:
        await state.finish()
        await message.answer(txt.ACCESS_TEXT)


@dp.message_handler(state=states.SetAdmin.s)
async def create_admin(message: types.Message, state: FSMContext):
    """ Function for sudo admin """
    s = message.text
    add.add_info(value=s, column='user_id', table='admin_panel')
    await state.finish()
    await message.answer(txt.DONE_TEXT)


@dp.message_handler(commands='apanel')
async def a_panel(message: types.Message, state: FSMContext):
    """ Function of admin registration """
    await state.reset_state()
    access = len(strip_list(str(connect.find_matches_where_two(data=int(message.from_user.id),
                                                               find_column_one='user_id',
                                                               find_column_two='user_password', table='admin_panel',
                                                               where_column='user_id'))))
    if access == 2:
        await states.EnterAdmin.e.set()
        await message.answer(txt.APASSWORD_TEXT, reply_markup=nav.o_cancel_menu)
    elif access == 1:
        await states.CreateApassword.c.set()
        await message.answer(txt.CREATE_PASSWORD_TEXT, reply_markup=nav.cancel_menu)
    else:
        await message.answer(txt.ACCESS_TEXT, reply_markup=nav.main_menu)


@dp.message_handler(state=states.CreateApassword.c)
async def create_a_password(message: types.Message, state: FSMContext):
    """ Function of create password for admin """
    c = message.text
    if c == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)
    elif 4 <= len(c) < 33 and c.find("'") < 0 and c.find(',') < 0:
        update.update_where(data_what=c, data_where=int(message.from_user.id), table_what='user_password',
                            table_where='user_id', table='admin_panel')
        await state.finish()
        await states.Apanel.a.set()
        await message.answer(txt.ACCEPT_PASSWORD_TEXT)
    else:
        await message.answer(txt.WRONG_TEXT)


@dp.message_handler(state=states.EnterAdmin.e)
async def a_password(message: types.Message, state: FSMContext):
    """ Function for enter admin enter your account """
    e = message.text
    if e == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)
    elif 4 <= len(e) < 33 and e.find("'") < 0:
        login = strip_list(str(connect.find_matches_where_two(data=message.from_user.id, find_column_one='user_id',
                                                              find_column_two='user_password', table='admin_panel',
                                                              where_column='user_id')))
        if int(login[0]) == int(message.from_user.id) and str(login[1]) == str(e):
            await state.finish()
            social_credit = str(strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id),
                                                                             find_column='social_credit',
                                                                             table='admin_panel',
                                                                             where_column='user_id'))))
            all_rating = strip_alist(str(connect.find_what_one(where='social_credit', table='admin_panel', flag=False)))
            all_data = strip_report(str(connect.find_what_where(data='False', where='id', table='cards_report',
                                                                bar='take', flag=False)))
            await states.Apanel.a.set()
            await message.answer(f"{txt.AENTER_TEXT_P1}{social_credit}{txt.AENTER_TEXT_P2}"
                                 f"{check_place(value_list=all_rating, data=all_rating)}{txt.AENTER_TEXT_P3}",
                                 reply_markup=nav.remove_markup)
            count = 0
            for i in all_data:
                if count < 6:
                    await message.answer(f"№{i}")
                else:
                    break
        else:
            await message.answer(txt.INCORRECT_TEXT)
    else:
        await message.answer(txt.WRONG_TEXT)


@dp.message_handler(commands='q', state=states.Apanel.a)
async def q(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Вы прекратили админиситрирование')


@dp.message_handler(commands='reports', state=states.Apanel.a)
async def reports(message: types.Message):
    count = 0
    await message.answer(txt.AVAILABLE_TEXT)
    for i in strip_report(str(connect.find_what_where(data='False', where='id', table='cards_report', bar='take',
                                                      flag=False))):
        if count < 6:
            await message.answer(f"№{i}")
        else:
            break
    count += 1


@dp.message_handler(commands='recon', state=states.Apanel.a)
async def admin(message: types.Message):
    """ Function of report """
    m = message.text
    m = m.split(' ')
    if len(m) == 2 and m[1].isdigit():
        report = strip_parentheses(str(connect.find_what_where(data=m[1], where='*', table='cards_report', bar='id',
                                                               flag=False)))
        print(report)
        if report:
            await message.answer(f"""Такой репорт найден!\n
            Номер человека: {report[1].replace("'", '')}
            Номер карты человека: {report[2].replace("'", '')}
            Ссылка на ВКонтакте: {report[3].replace("'", '')}
            ID в Telegram: {report[4].replace("'", '')}
            Имеющийся ID в БАЗЕ ДАННЫХ: {report[6].replace("'", '')}
            \nДоказательства (ПЕРЕХОДИТЕ ТОЛЬКО ПО ЮТУБ ССЫЛКАМ, ЭТО СДЕЛАНО ДЛЯ ВАШЕЙ БЕЗОПАСНОСТИ!): 
        {report[5].replace("'", '')}""")


@dp.message_handler(Text(equals='❌Отменить действие'))
async def cancel_action(message: types.Message, state: FSMContext):
    """ Function for cancel your action """
    await state.reset_state()
    delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
    await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)


@dp.message_handler(Text(equals='🔄Вернуться назад'))
async def back_actions(message: types.Message, state: FSMContext):
    """ Return your actions """
    await state.reset_state()
    delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
    await message.answer(txt.BACK_TEXT, reply_markup=nav.main_menu)


if __name__ == '__main__':
    Create()
    connect = FindUser()
    add = AddUser()
    delete = DeleteInfo()
    update = UpdateInfo()
    ClearMessages()
    print('[INFO] Modules launched successfully!')
    executor.start_polling(dp)
