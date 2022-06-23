#! /usr/bin/env python3.9
# Script for python version 3.9 and for Debian Linux
from aiogram import Bot, Dispatcher, executor, types
from src.bot.config import TOKEN, RED_ADMIN, RED_ADMIN_PASSWORD
from aiogram.dispatcher.filters import Text
import src.data.markup as nav
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.con_db.actions_db import FindUser, AddUser, DeleteInfo, UpdateInfo
import states
import src.data.text as txt
from instruments import strip_all, strip_list, check_place, strip_alist, strip_report, s_none, c_none, social_rating
from src.con_db.ClearMessages import ClearMessages
from src.con_db.Create import Create
from src.bot.instruments import strip_parentheses


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
    await states.FindUsers.f.set()
    await message.answer(txt.FIND_TEXT, reply_markup=nav.find_menu)


@dp.message_handler(state=states.FindUsers.f)
async def find_user_division(message: types.Message, state: FSMContext):
    """ Function of report """
    r = message.text
    if r == 'Проверить ссылку во ВКонтакте⛓':
        await state.finish()
        await states.FindShareVK.f.set()
        await message.reply(txt.VK_TEXT, reply_markup=nav.o_cancel_menu)

    elif r == '🆔Проверить по ID в Telegram':
        await state.finish()
        await states.FindIDTG.f.set()
        await message.reply(txt.TG_TEXT, reply_markup=nav.o_cancel_menu)

    elif r == '💳Проверить по номеру карты':
        await state.finish()
        await states.FindCardNumber.f.set()
        await message.reply(txt.CARD_TEXT, reply_markup=nav.o_cancel_menu)

    elif r == 'Проверить по номеру телефона📞':
        await state.finish()
        await states.FindTelephoneNumber.f.set()
        await message.reply(txt.TELEPHONE_TEXT, reply_markup=nav.o_cancel_menu)

    elif r == '🏠Проверить по адресу':
        await state.finish()
        await states.FindAddress.f.set()
        await message.reply(txt.ADDRESS_TEXT, reply_markup=nav.o_cancel_menu)

    elif r == '🔄Вернуться назад':
        await state.finish()
        await state.reset_state()
        await message.answer(txt.BACK_TEXT, reply_markup=nav.selections_menu)

    else:
        await message.reply(txt.ELSE_TEXT)


@dp.message_handler(state=states.FindShareVK.f)
async def find_share_vk(message: types.Message, state: FSMContext):
    """ Function for check user's VK's share """
    f = message.text
    if f == '❌Отменить действие':
        await state.finish()

        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    elif 15 < len(f) < 129 and (f[0:17] == txt.VK_CM or f[0:16] == txt.VK_CMN or f[0:15] == txt.VK_C or f[0:14] ==
                                txt.VK_CN) and f.find("'") < 0 and f.find(' ') < 0:
        matches = connect.find_matches(mean=f, column='share_vk')

        if matches[0]:
            await state.finish()
            all_data = strip_parentheses(str(connect.find_matches_where_one(data=f, find_column='*', table='cards_true',
                                                                            where_column='share_vk', flag=True)))
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}\n\nОстальные данные этого мошенника:\n'
                                f'Номер телефона: {c_none(all_data[1])}\n'
                                f'Номер карты: {c_none(all_data[2])}\n'
                                f'Ссылка во ВКонтакте: {c_none(all_data[3])}\n'
                                f'ID в Telegram: {c_none(all_data[4])}\n'
                                f'Адрес: {c_none(all_data[6])}\n',
                                reply_markup=nav.selections_menu)

        else:
            await state.finish()
            await message.reply(txt.NOT_FOUND, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


@dp.message_handler(state=states.FindIDTG.f)
async def find_share_tg(message: types.Message, state: FSMContext):
    """ Function for check user's Telegram's share """
    f = message.text
    if f == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    elif len(f) < 65 and f.find("'") < 0 and f.find(' ') < 0 and f[0] != '@':
        matches = connect.find_matches(mean=f, column='share_tg')

        if matches[0]:
            await state.finish()
            all_data = strip_parentheses(str(connect.find_matches_where_one(data=f, find_column='*', table='cards_true',
                                                                            where_column='share_tg', flag=True)))
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}\n\nОстальные данные этого мошенника:\n'
                                f'Номер телефона: {c_none(all_data[1])}\n'
                                f'Номер карты: {c_none(all_data[2])}\n'
                                f'Ссылка во ВКонтакте: {c_none(all_data[3])}\n'
                                f'ID в Telegram: {c_none(all_data[4])}\n'
                                f'Адрес: {c_none(all_data[6])}\n',
                                reply_markup=nav.selections_menu)

        else:
            await state.finish()
            await message.reply(txt.NOT_FOUND, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


@dp.message_handler(state=states.FindCardNumber.f)
async def find_card(message: types.Message, state: FSMContext):
    """ Function for check user's card number's share """
    f = message.text
    if f == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    elif len(f) == 16 and f.isdigit():
        matches = connect.find_matches(mean=f, column='cnumber')

        if matches[0]:
            await state.finish()
            all_data = strip_parentheses(str(connect.find_matches_where_one(data=f, find_column='*', table='cards_true',
                                                                            where_column='cnumber', flag=True)))
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}\n\nОстальные данные этого мошенника:\n'
                                f'Номер телефона: {c_none(all_data[1])}\n'
                                f'Номер карты: {c_none(all_data[2])}\n'
                                f'Ссылка во ВКонтакте: {c_none(all_data[3])}\n'
                                f'ID в Telegram: {c_none(all_data[4])}\n'
                                f'Адрес: {c_none(all_data[6])}\n',
                                reply_markup=nav.selections_menu)

        else:
            await state.finish()
            await message.reply(txt.NOT_FOUND, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


@dp.message_handler(state=states.FindTelephoneNumber.f)
async def find_telephone(message: types.Message, state: FSMContext):
    """ Function for check user's telephone number's share """
    f = message.text
    if f == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    elif len(f) < 17 and f.find("'") < 0 and f[0] == '+' and f.find(' ') < 0:
        matches = connect.find_matches(mean=f, column='tnumber')

        if matches[0]:
            await state.finish()
            all_data = strip_parentheses(str(connect.find_matches_where_one(data=f, find_column='*', table='cards_true',
                                                                            where_column='tnumber', flag=True)))
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}\n\nОстальные данные этого мошенника:\n'
                                f'Номер телефона: {c_none(all_data[1])}\n'
                                f'Номер карты: {c_none(all_data[2])}\n'
                                f'Ссылка во ВКонтакте: {c_none(all_data[3])}\n'
                                f'ID в Telegram: {c_none(all_data[4])}\n'
                                f'Адрес: {c_none(all_data[6])}\n',
                                reply_markup=nav.selections_menu)

        else:
            await state.finish()
            await message.reply(txt.NOT_FOUND, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


@dp.message_handler(state=states.FindAddress.f)
async def find_address(message: types.Message, state: FSMContext):
    """ Function for check user's address's share """
    f = message.text
    if f == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    elif f.find("'") < 0 and f.find(' ') < 0 and 16 < len(f) < 1025 and f.find(',') < 0:
        matches = connect.find_matches(mean=f, column='address')

        if matches[0]:
            await state.finish()
            all_data = strip_parentheses(str(connect.find_matches_where_one(data=f, find_column='*', table='cards_true',
                                                                            where_column='address', flag=True)))
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}\n\nОстальные данные этого мошенника:\n'
                                f'Номер телефона: {c_none(all_data[1])}\n'
                                f'Номер карты: {c_none(all_data[2])}\n'
                                f'Ссылка во ВКонтакте: {c_none(all_data[3])}\n'
                                f'ID в Telegram: {c_none(all_data[4])}\n'
                                f'Адрес: {c_none(all_data[6])}\n',
                                reply_markup=nav.selections_menu)

        else:
            await state.finish()
            await message.reply(txt.NOT_FOUND, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


@dp.message_handler(Text(equals='Подать жалобу на внесение в ЧС➕'))
async def add_user(message: types.Message):
    """ Function for add user in black list """
    await states.DoReport.r.set()
    await message.answer(txt.ADD_TEXT, reply_markup=nav.report_menu)


@dp.message_handler(Text(equals='Подать жалобу на удаление из ЧС➖'))
async def delete_user(message: types.Message):
    """ Function for delete user from black list """
    await states.NotDo.n.set()
    await message.answer(txt.DELETE_TEXT, reply_markup=nav.o_cancel_menu)


@dp.message_handler(state=states.NotDo.n)
async def delete_user(message: types.Message, state: FSMContext):
    """ Function for ask id from black list """
    n = message.text
    if n == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)
    elif n.isdigit():
        find = strip_parentheses(str(connect.find_matches_where_one(find_column='*', table='cards_true',
                                                                    where_column='id', data=int(n), flag=True)))
        if str(find) != "['None']":
            await state.finish()
            await message.answer(f"ID админа, занёсшего пользователя в чёрный список: "
                                 f"{find[-1]}\nПричина, по которой выбранного пользователя занесли в чёрный "
                                 f"""список: {find[-3].replace("'", '')}\n\nПродолжить подачу жалобы?""",
                                 reply_markup=nav.yesno_menu)
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=n, first_column='user_id',
                        second_column='message', table='messages')
            await states.Continue.c.set()
        else:
            await message.answer(txt.ID_NFIND)
    else:
        await message.reply(txt.ELSE_TEXT)


@dp.message_handler(state=states.Continue.c)
async def continue_(message: types.Message, state: FSMContext):
    """ Asking for a sequel """
    c = message.text
    if c == '❌Отменить действие':
        await state.finish()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)
    elif c == '👍Да':
        await state.finish()
        await message.answer(txt.DOC_TEXT, reply_markup=nav.o_cancel_menu)
        await states.AddDocsDelete.a.set()
    elif c == '👎Нет':
        await state.finish()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.BACK_TEXT, reply_markup=nav.main_menu)


@dp.message_handler(state=states.AddDocsDelete.a)
async def add_docs_delete(message: types.Message, state: FSMContext):
    """ Function for adding evidence for removal from the black list """
    a = message.text
    if a == '❌Отменить действие':
        await state.finish()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)
    elif 22 < len(a) < 256 and (a[0:24] == txt.YOUTUBE_C or a[0:23] == txt.YOUTUBE_CN or a[0:22] == txt.YOUTUBE_CM or
                                a[0:21] == txt.YOUTUBE_CMN or a[0:17] == txt.YOUTUBE_BEC or a[0:16] == txt.YOUTUBE_BECN
                                or a[0:19] == txt.YOUTUBE_BEMC or a[0:18] == txt.YOUTUBE_BEMCN or a[0:20] ==
                                txt.YOUTUBE_NW or a[0:19] == txt.YOUTUBE_NNW or a[0:22] == txt.YOUTUBE_NWM or a[0:21]
                                == txt.YOUTUBE_NNWM) and a.find("'") < 0 and a.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id', flag=True)))
        add.add_two(first_value=a, second_value=data, first_column='docers',
                    second_column='delete', table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)
    else:
        await message.reply(txt.ELSE_TEXT)


@dp.message_handler(state=states.DoReport.r)
async def do_report(message: types.Message, state: FSMContext):
    """ Function of report """
    r = message.text
    if r == 'Проверить ссылку во ВКонтакте⛓':
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

    elif r == 'Проверить по номеру телефона📞':
        await state.finish()
        await states.TelephoneNumber.t.set()
        await message.reply(txt.TELEPHONE_TEXT, reply_markup=nav.cancel_menu)

    elif r == '🏠Проверить по адресу':
        await state.finish()
        await states.Address.a.set()
        await message.reply(txt.ADDRESS_TEXT, reply_markup=nav.cancel_menu)

    elif r == 'У меня есть ID мошенника из базы данных🧾':
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
            all_data = strip_parentheses(str(connect.find_matches_where_one(data=s, find_column='*', table='cards_true',
                                                                            where_column='share_vk', flag=True)))
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}\n\nОстальные данные этого мошенника:\n'
                                f'Номер телефона: {c_none(all_data[1])}\n'
                                f'Номер карты: {c_none(all_data[2])}\n'
                                f'Ссылка во ВКонтакте: {c_none(all_data[3])}\n'
                                f'ID в Telegram: {c_none(all_data[4])}\n'
                                f'Адрес: {c_none(all_data[6])}\n',
                                reply_markup=nav.selections_menu)
        else:
            await state.finish()
            await states.YesNoVK.y.set()
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=s, first_column='user_id',
                        second_column='message', table='messages')
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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
                                or n[0:19] == txt.YOUTUBE_BEMC or n[0:18] == txt.YOUTUBE_BEMCN or n[0:20] ==
                                txt.YOUTUBE_NW or n[0:19] == txt.YOUTUBE_NNW or n[0:22] == txt.YOUTUBE_NWM or n[0:21]
                                == txt.YOUTUBE_NNWM) and n.find("'") < 0 and n.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id', flag=True)))
        add.add_two(first_value=n, second_value=data, first_column='docers',
                    second_column='share_vk', table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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

    elif len(i) < 65 and i.find("'") < 0 and i.find(' ') < 0 and i[0] != '@':
        matches = connect.find_matches(mean=i, column='share_tg')

        if matches[0]:
            await state.finish()
            all_data = strip_parentheses(str(connect.find_matches_where_one(data=i, find_column='*', table='cards_true',
                                                                            where_column='share_tg', flag=True)))
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}\n\nОстальные данные этого мошенника:\n'
                                f'Номер телефона: {c_none(all_data[1])}\n'
                                f'Номер карты: {c_none(all_data[2])}\n'
                                f'Ссылка во ВКонтакте: {c_none(all_data[3])}\n'
                                f'ID в Telegram: {c_none(all_data[4])}\n'
                                f'Адрес: {c_none(all_data[6])}\n',
                                reply_markup=nav.selections_menu)
        else:
            await state.finish()
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=i, first_column='user_id',
                        second_column='message', table='messages')
            await states.YesNoTG.y.set()
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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
                                or n[0:19] == txt.YOUTUBE_BEMC or n[0:18] == txt.YOUTUBE_BEMCN or n[0:20] ==
                                txt.YOUTUBE_NW or n[0:19] == txt.YOUTUBE_NNW or n[0:22] == txt.YOUTUBE_NWM or n[0:21]
                                == txt.YOUTUBE_NNWM) and n.find("'") < 0 and n.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id', flag=True)))
        add.add_two(first_value=n, second_value=data, first_column='docers',
                    second_column='share_tg', table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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

    elif len(c) == 16 and c.isdigit():
        matches = connect.find_matches(mean=int(c), column='cnumber')

        if matches[0]:
            await state.finish()
            all_data = strip_parentheses(str(connect.find_matches_where_one(data=c, find_column='*', table='cards_true',
                                                                            where_column='cnumber', flag=True)))
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}\n\nОстальные данные этого мошенника:\n'
                                f'Номер телефона: {c_none(all_data[1])}\n'
                                f'Номер карты: {c_none(all_data[2])}\n'
                                f'Ссылка во ВКонтакте: {c_none(all_data[3])}\n'
                                f'ID в Telegram: {c_none(all_data[4])}\n'
                                f'Адрес: {c_none(all_data[6])}\n',
                                reply_markup=nav.selections_menu)
        else:
            await state.finish()
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=int(c), first_column='user_id',
                        second_column='message', table='messages')
            await states.YesNoCard.y.set()
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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
        await message.reply(txt.WRONG_TEXT)


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
                                or n[0:19] == txt.YOUTUBE_BEMC or n[0:18] == txt.YOUTUBE_BEMCN or n[0:20] ==
                                txt.YOUTUBE_NW or n[0:19] == txt.YOUTUBE_NNW or n[0:22] == txt.YOUTUBE_NWM or n[0:21]
                                == txt.YOUTUBE_NNWM) and n.find("'") < 0 and n.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id', flag=True)))
        add.add_two(first_value=n, second_value=int(data), first_column='docers', second_column='cnumber',
                    table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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
            all_data = strip_parentheses(str(connect.find_matches_where_one(data=t, find_column='*', table='cards_true',
                                                                            where_column='tnumber', flag=True)))
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}\n\nОстальные данные этого мошенника:\n'
                                f'Номер телефона: {c_none(all_data[1])}\n'
                                f'Номер карты: {c_none(all_data[2])}\n'
                                f'Ссылка во ВКонтакте: {c_none(all_data[3])}\n'
                                f'ID в Telegram: {c_none(all_data[4])}\n'
                                f'Адрес: {c_none(all_data[6])}\n',
                                reply_markup=nav.selections_menu)
        else:
            await state.finish()
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=t, first_column='user_id',
                        second_column='message', table='messages')
            await states.YesNoTelephone.y.set()
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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
        await message.reply(txt.WRONG_TEXT)


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
                                or n[0:19] == txt.YOUTUBE_BEMC or n[0:18] == txt.YOUTUBE_BEMCN or n[0:20] ==
                                txt.YOUTUBE_NW or n[0:19] == txt.YOUTUBE_NNW or n[0:22] == txt.YOUTUBE_NWM or n[0:21]
                                == txt.YOUTUBE_NNWM) and n.find("'") < 0 and n.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id', flag=True)))
        add.add_two(first_value=n, second_value=data, first_column='docers',
                    second_column='tnumber', table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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
        if connect.find_matches_where_one(data=int(i), find_column='id', table='cards_true', where_column='id',
                                          flag=True):
            await state.finish()
            await message.answer(txt.DOC_TEXT, reply_markup=nav.o_cancel_menu)
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=int(i), first_column='user_id',
                        second_column='message', table='messages')
            await states.DocsCard.d.set()
        else:
            await message.reply(txt.NO_ID, reply_markup=nav.o_cancel_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


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
                                or d[0:19] == txt.YOUTUBE_BEMC or d[0:18] == txt.YOUTUBE_BEMCN or d[0:20] ==
                                txt.YOUTUBE_NW or d[0:19] == txt.YOUTUBE_NNW or d[0:22] == txt.YOUTUBE_NWM or d[0:21]
                                == txt.YOUTUBE_NNWM) and d.find("'") < 0 and d.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id', flag=True)))
        add.add_two(first_value=d, second_value=int(data), first_column='docers',
                    second_column='got_id', table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


@dp.message_handler(state=states.Address.a)
async def check_address(message: types.Message, state: FSMContext):
    """ This function ask user swindler's house """
    a = message.text
    a = a.replace('—', '-').replace('–', '-').replace('−', '-').replace('-', '-').lower()
    if a == '❌Отменить действие':
        await state.finish()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)

    elif 16 < len(a) < 1025 and a.find(',') < 0 and a.count('|') == 4 and a.find("'") < 0:
        matches = connect.find_matches(mean=a, column='address')

        if matches[0]:
            await state.finish()
            all_data = strip_parentheses(str(connect.find_matches_where_one(data=a, find_column='*', table='cards_true',
                                                                            where_column='address', flag=True)))
            await message.reply(f'{txt.USER_FIND_TEXT_P1} {strip_all(str(matches[1]))}'
                                f'{txt.USER_FIND_TEXT_P2}\n\nОстальные данные этого мошенника:\n'
                                f'Номер телефона: {c_none(all_data[1])}\n'
                                f'Номер карты: {c_none(all_data[2])}\n'
                                f'Ссылка во ВКонтакте: {c_none(all_data[3])}\n'
                                f'ID в Telegram: {c_none(all_data[4])}\n'
                                f'Адрес: {c_none(all_data[6])}\n',
                                reply_markup=nav.selections_menu)

        else:
            await state.finish()
            delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
            add.add_two(first_value=int(message.from_user.id), second_value=a, first_column='user_id',
                        second_column='message', table='messages')
            await states.YesNoAddress.y.set()
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


@dp.message_handler(state=states.YesNoAddress.y)
async def yes_no_address(message: types.Message, state: FSMContext):
    """ Function for ask about docs """
    y = message.text
    if y == '👍Да':
        await state.finish()
        await states.DoReport.r.set()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.YES_TEXT, reply_markup=nav.report_menu)

    elif y == '👎Нет':
        await state.finish()
        await states.NoAddress.n.set()
        await message.answer(txt.DOC_TEXT, reply_markup=nav.o_cancel_menu)

    elif y == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


@dp.message_handler(state=states.NoAddress.n)
async def add_docs_address(message: types.Message, state: FSMContext):
    """ This function add proofs in database """
    n = message.text
    if n == '❌Отменить действие':
        await state.finish()
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.main_menu)

    elif 22 < len(n) < 256 and (n[0:24] == txt.YOUTUBE_C or n[0:23] == txt.YOUTUBE_CN or n[0:22] == txt.YOUTUBE_CM or
                                n[0:21] == txt.YOUTUBE_CMN or n[0:17] == txt.YOUTUBE_BEC or n[0:16] == txt.YOUTUBE_BECN
                                or n[0:19] == txt.YOUTUBE_BEMC or n[0:18] == txt.YOUTUBE_BEMCN or n[0:20] ==
                                txt.YOUTUBE_NW or n[0:19] == txt.YOUTUBE_NNW or n[0:22] == txt.YOUTUBE_NWM or n[0:21]
                                == txt.YOUTUBE_NNWM) and n.find("'") < 0 and n.find(' ') < 0:
        await state.finish()
        data = strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='message',
                                                            table='messages', where_column='user_id', flag=True)))
        add.add_two(first_value=n, second_value=data, first_column='docers',
                    second_column='address', table='cards_report')
        delete.delete_where(data=int(message.from_user.id), table='messages', column='user_id')
        await message.answer(txt.DOCS_TEXT, reply_markup=nav.main_menu)

    else:
        await message.reply(txt.WRONG_TEXT)


@dp.message_handler(commands='ahelp')
async def a_help(message: types.Message):
    """ Function of admins' help """
    if connect.find_matches_where_one(data=int(message.from_user.id), find_column='user_id', table='admin_panel',
                                      where_column='user_id', flag=True):
        await message.answer(txt.ADMIN_HELP_TEXT, reply_markup=nav.main_menu)
    else:
        await message.answer(txt.ACCESS_TEXT)


@dp.message_handler(commands='sudo')
async def set_admin(message: types.Message, state: FSMContext):
    """ Function for set admins in database """
    await state.reset_state()
        if int(message.from_user.id) == (int(RED_ADMIN_0) or int(RED_ADMIN_1)):  # Refactor this line and .env if you want
        # ...remove or add red admin
        await states.SetAdminPassword.s.set()
        await message.answer(txt.SUDO_TEXT, reply_markup=nav.remove_markup)
    else:
        await message.answer(txt.ACCESS_TEXT)


@dp.message_handler(state=states.SetAdminPassword.s)
async def enter_admin_password(message: types.Message, state: FSMContext):
    """ Function for sudo admin """
    s = message.text
    if str(s) == (str(RED_ADMIN_PASSWORD_0) or str(RED_ADMIN_PASSWORD_1)):  # And this line
        await state.finish()
        await states.Sudo.s.set()
        await message.answer(txt.SET_ADMIN_TEXT)
    else:
        await state.finish()
        await message.answer(txt.ACCESS_TEXT)


@dp.message_handler(commands='sudo', state=states.Sudo.s)
async def sudo(message: types.Message, state: FSMContext):
    """ Function for sudo admin """
    m = message.text
    m = m.split(' ')
    len_m = len(m)
    if len_m == 3 and m[1].lower() == 'add' and m[2].isdigit():
        add.add_info(table='admin_panel', column='user_id', value=int(m[2]))
        await state.finish()
        await message.answer(txt.ADD_ADMIN_TEXT, reply_markup=nav.main_menu)
    elif len_m == 3 and m[1].lower() == 'delete' and m[2].isdigit():
        delete.delete_where(table='admin_panel', column='user_id', data=int(m[2]))
        await state.finish()
        await message.answer(txt.DELETE_ADMIN_TEXT, reply_markup=nav.main_menu)
    elif len_m == 2 and m[1].lower() == 'all':
        await state.finish()
        await message.answer(txt.ALL_TEXT)
        await message.answer(str(connect.find_what_one(where='*', table='admin_panel',
                                                       flag=False)).replace('), (', '\n'),
                             reply_markup=nav.main_menu)
    elif len_m == 3 and m[1].lower() == 'passwd' and m[2].isdigit():
        await state.finish()
        update.update_where(table='admin_panel', table_what='user_password', data_what='', table_where='user_id',
                            data_where=int(m[2]))
        await message.answer(txt.PASSWD_TEXT)
    elif m[1] == 'q':
        await state.finish()
        await message.answer(txt.QUIT_TEXT, reply_markup=nav.main_menu)
    else:
        await state.finish()
        await message.answer(txt.ACCESS_TEXT)


@dp.message_handler(commands='apanel')
async def a_panel(message: types.Message, state: FSMContext):
    """ Function of admin registration """
    await state.reset_state()
    access = len(strip_list(str(connect.find_matches_where_two(data=int(message.from_user.id),
                                                               find_column_one='user_id',
                                                               find_column_two='user_password', table='admin_panel',
                                                               where_column='user_id', flag=True))))
    if access == 2 and strip_all(str(connect.find_matches_where_one(find_column='user_password', table='admin_panel',
                                                                    where_column='user_id',
                                                                    data=int(message.from_user.id), flag=True))):
        await states.EnterAdmin.e.set()
        await message.answer(txt.APASSWORD_TEXT, reply_markup=nav.o_cancel_menu)
    elif access == 1 or access == 2:
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
                                                              where_column='user_id', flag=True)))
        if int(login[0]) == int(message.from_user.id) and str(login[1]) == str(e):
            await state.finish()
            social_credit = str(strip_all(str(connect.find_matches_where_one(data=int(message.from_user.id),
                                                                             find_column='social_credit',
                                                                             table='admin_panel',
                                                                             where_column='user_id', flag=True))))
            all_rating = strip_alist(str(connect.find_what_one(where='social_credit', table='admin_panel', flag=False)))
            all_data = strip_report(str(connect.find_matches_where_one(data=False, find_column='id',
                                                                       table='cards_report', where_column='take',
                                                                       flag=False)))
            await states.Apanel.a.set()
            await message.answer(f"{txt.AENTER_TEXT_P1}{social_credit}{txt.AENTER_TEXT_P2}"
                                 f"{check_place(value_list=all_rating, data=all_rating)}{txt.AENTER_TEXT_P3}",
                                 reply_markup=nav.remove_markup)
            for i in all_data:
                if len(all_data) == 0:
                    await message.answer(txt.GOOD_WORK_TEXT)
                else:
                    count = 0
                    if count < 6:
                        await message.answer(f"№{i}")
                        count += 1
                    else:
                        break
        else:
            await message.answer(txt.INCORRECT_TEXT)
    else:
        await message.answer(txt.WRONG_TEXT)


@dp.message_handler(commands='q', state=states.Apanel.a)
async def q(message: types.Message, state: FSMContext):
    """ Function for quit from admin's account """
    await state.finish()
    await message.answer('Вы прекратили администрирование!', reply_markup=nav.main_menu)


@dp.message_handler(commands='reports', state=states.Apanel.a)
async def reports(message: types.Message):
    """ Function for check all reports """
    await message.answer(txt.AVAILABLE_TEXT)
    all_data = strip_report(str(connect.find_matches_where_one(data=False, find_column='id', table='cards_report',
                                                               where_column='take', flag=False)))
    for i in all_data:
        if len(all_data) == 0:
            await message.answer(txt.GOOD_WORK_TEXT)
        else:
            count = 0
            if count < 6:
                await message.answer(f"№{i}")
                count += 1
            else:
                break


@dp.message_handler(commands='recon', state=states.Apanel.a)
async def admin(message: types.Message, state: FSMContext):
    """ Function of report """
    m = message.text
    m = m.split(' ')
    if len(m) == 2 and m[1].isdigit() and str(connect.find_matches_where_one(data=m[1], find_column='take',
                                                                             table='cards_report', where_column='id',
                                                                             flag=True)) == '(False,)':
        report = strip_parentheses(str(connect.find_matches_where_one(data=m[1], find_column='*', table='cards_report',
                                                                      where_column='id', flag=True)))
        delete_id = report[-2]
        if str(report) != "['[]']" and delete_id is None:
            await state.finish()
            await message.answer(f"""ЭТО РПЕОРТ НА ДОБАВЛЕНИЕ ЧЕЛОВЕКА В ЧЁРНЫЙ СПИСОК!\n
            Номер телефона человека: {report[1].replace("'", '')}
            Номер карты человека: {report[2].replace("'", '')}
            Ссылка на ВКонтакте: {report[3].replace("'", '')}
            ID в Telegram: {report[4].replace("'", '')}
            Имеющийся ID в БАЗЕ ДАННЫХ (Информация дополнится к ЧС-нику): {report[6].replace("'", '')}
            Адрес человека: {report[10].replace("'", '')}
            \nДоказательства (ПЕРЕХОДИТЕ ТОЛЬКО ПО ЮТУБ ССЫЛКАМ, ЭТО СДЕЛАНО ДЛЯ ВАШЕЙ БЕЗОПАСНОСТИ!): 
        {report[5].replace("'", '')}\n
/accept - принять жалобу (Если форма заполнена правильно и док-ва не являются подделкой)
/cancel - отвергнуть жалобу (Если форма заполнена неправильно и док-ва являются подделкой)
/acrib - шпаргалка по заполнению пунктов""")
            update.update_where(data_what=True, data_where=m[1], table_what='take', table_where='id',
                                table='cards_report')
            update.update_where(data_what=int(message.from_user.id), data_where=m[1], table_what='admin_take',
                                table_where='id', table='cards_report')
            await states.AcceptAdd.a.set()
        elif str(report) != "['[]']" and delete_id is not None and delete_id.isdigit():
            await state.finish()
            all_data = connect.find_matches_where_one(find_column='*', table='cards_true', where_column='id',
                                                      data=int(delete_id), flag=False)
            await message.answer(f"""ЭТО РПЕОРТ НА УДАЛЕНИЕ ЧЕЛОВЕКА ИЗ ЧЁРНОГО СПИСКА\n
            ID человека в базе данных: {int(delete_id)}
            Номер телефона человека: {all_data[2].replace("'", '')}
            Номер карты человека: {all_data[3].replace("'", '')}
            Ссылка на ВКонтакте: {all_data[4].replace("'", '')}
            ID в Telegram: {all_data[5].replace("'", '')}
            Адрес человека: {all_data[-2].replace("'", '')}
            \nПричина, по которой человек был занесён в ЧС (ПЕРЕХОДИТЕ ТОЛЬКО ПО ЮТУБ ССЫЛКАМ, ЭТО СДЕЛАНО ДЛЯ ВАШЕЙ
             БЕЗОПАСНОСТИ!): {all_data[-3].replace("'", '')}
             Доказательства предоставленные человеком, для вынесения: {report[5].replace("'", '')}\n
/accept - принять жалобу (Если форма заполнена правильно и док-ва не являются подделкой)
/cancel - отвергнуть жалобу (Если форма заполнена неправильно и док-ва являются подделкой)
/acrib - шпаргалка по заполнению пунктов""")
            update.update_where(data_what=True, data_where=m[1], table_what='take', table_where='id',
                                table='cards_report')
            update.update_where(data_what=int(message.from_user.id), data_where=m[1], table_what='admin_take',
                                table_where='id', table='cards_report')
            await states.AcceptDelete.a.set()
        else:
            await message.answer(txt.NOT_REPORT_TEXT)
    else:
        await message.answer(txt.NOT_REPORT_TEXT)


@dp.message_handler(commands='check', state=states.Apanel.a)
async def a_check(message: types.Message):
    """ Function to check scammer data in database """
    c = message.text
    c = c.split(' ')
    if len(c) == 2 and c[1].isdigit():
        data = strip_parentheses(str(connect.find_matches_where_one(find_column='*', table='cards_true',
                                                                    where_column='id', data=int(c[1]), flag=True)))
        if str(data) != "['None']":
            await message.answer(f"""Номер телефона: {data[1].replace("'", '')}
Номер карты: {data[2].replace("'", '')}
Ссылка во ВКонтакте: {data[3].replace("'", '')}
ID в Telegram: {data[4].replace("'", '')}
Адрес: {data[6].replace("'", '')}
Причина: {data[-3].replace("'", '')}
Админ, рассмотревший жалобу: {data[-1].replace("'", '')}""")
        else:
            await message.answer('Такой ID отсутствует!')
    else:
        await message.answer('Неправильный формат сообщения!')


@dp.message_handler(commands='accept', state=states.AcceptDelete.a)
async def accept_report_delete(message: types.Message, state: FSMContext):
    """ Function for accepting report """
    report = strip_parentheses(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='*',
                                                                  table='cards_report', where_column='admin_take',
                                                                  flag=True)))
    delete.delete_where(table='cards_true', column='id', data=int(report[-2]))
    delete.delete_where(data=int(message.from_user.id), column='admin_take', table='cards_report')
    await social_rating(message)
    await state.finish()
    await states.Apanel.a.set()
    await message.answer('Репорт был одобрен!')


@dp.message_handler(commands='accept', state=states.AcceptAdd.a)
async def accept_report(message: types.Message, state: FSMContext):
    """ Function for accepting report """
    report = strip_parentheses(str(connect.find_matches_where_one(data=int(message.from_user.id), find_column='*',
                                                                  table='cards_report', where_column='admin_take',
                                                                  flag=True)))
    add.add_all(first_data=s_none(report[1].replace("'", '')), second_data=s_none(report[2].replace("'", '')),
                third_data=s_none(report[3].replace("'", '')), fourth_data=s_none(report[4].replace("'", '')),
                fifth_data=s_none(report[5].replace("'", '')), sixth_data=s_none(report[10].replace("'", '')),
                seventh_data=s_none(report[8].replace("'", '')),
                first_column='tnumber', second_column='cnumber', third_column='share_vk', fourth_column='share_tg',
                fifth_column='docers', sixth_column='address', seventh_column='admin_take', table='cards_true')
    delete.delete_where(data=int(message.from_user.id), column='admin_take', table='cards_report')
    await social_rating(message)
    await state.finish()
    await states.Apanel.a.set()
    await message.answer('Репорт был одобрен!')


@dp.message_handler(commands='cancel', state=[states.AcceptAdd.a, states.AcceptDelete.a])
async def cancel_report(message: types.Message, state: FSMContext):
    """ Function for cancel report """
    await state.finish()
    await states.Apanel.a.set()
    delete.delete_where(table='cards_report', column='admin_take', data=int(message.from_user.id))
    await social_rating(message)
    await message.answer('Репорт был отклонён!')


@dp.message_handler(commands='change', state=[states.AcceptAdd.a, states.AcceptDelete.a])
async def change_report(message: types.Message):
    """ Function for change data of report """
    a = message.text
    a = a.split(' ')
    len_a = len(a)
    if len_a == 3 and a[1].lower() == 'telephone' and a[2].find(',') < 0 and a[2][0] == '+':
        update.update_where(table='cards_report', table_what='tnumber', data_what=a[2], table_where='admin_take',
                            data_where=int(message.from_user.id))
        await message.answer(txt.UPDATE_TEXT)

    elif len_a == 3 and a[1].lower() == 'card' and a[2].find(',') < 0 and len(a[2]) < 14:
        update.update_where(table='cards_report', table_what='cnumber', data_what=a[2], table_where='admin_take',
                            data_where=int(message.from_user.id))
        await message.answer(txt.UPDATE_TEXT)

    elif len_a == 3 and a[1].lower() == 'vk' and a[2].find(',') < 0 and (a[0:17] == txt.VK_CM or a[0:16] == txt.VK_CMN
                                                                         or a[0:15] == txt.VK_C or
                                                                         a[0:14] == txt.VK_CN):
        update.update_where(table='cards_report', table_what='share_vk', data_what=a[2], table_where='admin_take',
                            data_where=int(message.from_user.id))
        await message.answer(txt.UPDATE_TEXT)

    elif len_a == 3 and a[1].lower() == 'tg' and a[2].find(',') < 0 and a[2][0] != '@':
        update.update_where(table='cards_report', table_what='share_tg', data_what=a[2], table_where='admin_take',
                            data_where=int(message.from_user.id))
        await message.answer(txt.UPDATE_TEXT)

    elif len_a == 3 and a[1].lower() == 'id' and a[2].find(',') < 0 and a[2].isdigit():
        update.update_where(table='cards_report', table_what='got_id', data_what=a[2], table_where='admin_take',
                            data_where=int(message.from_user.id))
        await message.answer(txt.UPDATE_TEXT)
    else:
        await message.answer(txt.WRONG_TEXT)


@dp.message_handler(commands='acrib', state=[states.AcceptAdd.a, states.Apanel.a, states.AcceptDelete.a])
async def change_report(message: types.Message):
    """ Crib for admins """
    await message.answer(txt.CRIB)


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
