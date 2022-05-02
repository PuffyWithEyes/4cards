# Script for python version 3.9
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from aiogram.dispatcher.filters import Text
import data.markup as nav
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from con_db.actions_db import FindUser
import states
import data.text as txt


# Global settings for the bot
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
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


@dp.message_handler(Text(equals='❌Отменить действие'))
async def cancel_action(message: types.Message, state: FSMContext):
    """ Function for cancel your action """
    await state.reset_state()
    await message.answer(txt.CANCEL_TEXT)


@dp.message_handler(Text(equals='🔄Вернуться назад'))
async def back_actions(message: types.Message, state: FSMContext):
    """ Return your actions """
    await state.reset_state()
    await message.answer(txt.BACK_TEXT, reply_markup=nav.main_menu)


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
        await message.reply(txt.TG_TEXT)
    elif r == '💳Проверить по номеру карты':
        await state.finish()
        await states.CardNumber.c.set()
        await message.reply(txt.CARD_TEXT)
    elif r == '📞Проверить по номеру телефона':
        await state.finish()
        await states.TelephoneNumber.t.set()
        await message.reply(txt.TELEPHONE_TEXT)
    elif r == '🏠Проверить по адресу':
        await state.finish()
        await states.Address.a.set()
        await message.reply(txt.TELEPHONE_TEXT)
    elif r == '🧾У меня есть ID мошенника из базы данных':
        await state.finish()
        await states.ID.i.set()
        await message.reply(txt.ID_TEXT)
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
        
    elif len(s) < 129:
        matches = connect.find_matches(mean=s, column='share_vk')
        if matches[0]:
            await state.finish()
            await states.YesNo.y.set()
            await message.reply(f'{txt.USER_FIND_TEXT_P1} <b>{str(matches[1]).lstrip("(").rstrip(",)")}</b>'
                                f'{txt.USER_FIND_TEXT_P2}', reply_markup=nav.selections_menu)
        else:
            await state.finish()
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.selections_menu)

    else:
        await message.reply(txt.LONG_TEXT, reply_markup=nav.selections_menu)


@dp.message_handler(state=states.ReportIDTG.i)
async def check_tg(message: types.Message, state: FSMContext):
    """ Function for check matches """
    s = message.text
    if s == '❌Отменить действие':
        await state.finish()
        await message.answer(txt.CANCEL_TEXT, reply_markup=nav.selections_menu)

    elif s == '🔄Вернуться назад':
        await state.finish()
        await message.answer(txt.BACK_TEXT, reply_markup=nav.selections_menu)

    elif len(s) < 65:
        matches = connect.find_matches(mean=s, column='share_tg')
        if matches[0]:
            await state.finish()
            await states.YesNo.y.set()
            await message.reply(f'{txt.USER_FIND_TEXT_P1}<b>{str(matches[1]).lstrip("(").rstrip(",)")}</b>'
                                f'{txt.USER_FIND_TEXT_P2}', reply_markup=nav.selections_menu)
        else:
            await state.finish()
            await message.reply(txt.USER_NFIND_TEXT, reply_markup=nav.yesno_menu)

    else:
        await message.reply(txt.LONG_TEXT, reply_markup=nav.selections_menu)


@dp.message_handler(state=states.YesNo.y)
async def add_info(message: types.Message, state: FSMContext):
    y = message.text
    if y == '👍Да':
        await state.finish()
        await message.answer(txt.YES_TEXT, reply_markup=nav.report_menu)
    elif y == '👎Нет':
        await state.finish()
        await message.answer(txt.DOC_TEXT)


if __name__ == '__main__':
    connect = FindUser()
    executor.start_polling(dp)
