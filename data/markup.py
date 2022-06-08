""" Buttons for Telegram-bot """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


btn_info = KeyboardButton('ℹИнформация')
btn_report = KeyboardButton('📝Подать жалобу')
btn_search = KeyboardButton('🔭Найти пользователя')
btn_cancel = KeyboardButton('❌Отменить действие')
btn_VK = KeyboardButton('⛓Проверить ссылку во ВКонтакте')
btn_TG = KeyboardButton('🆔Проверить по ID в Telegram')
btn_card = KeyboardButton('💳Проверить по номеру карты')
btn_telephone = KeyboardButton('📞Проверить по номеру телефона')
btn_address = KeyboardButton('🏠Проверить по адресу')
btn_add = KeyboardButton('➕Подать жалобу на внесение в ЧС')
btn_delete = KeyboardButton('➖Подать жалобу на удаление из ЧС')
btn_back = KeyboardButton('🔄Вернуться назад')
btn_yes = KeyboardButton('👍Да')
btn_no = KeyboardButton('👎Нет')
btn_id = KeyboardButton('🧾У меня есть ID мошенника из базы данных')


main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_search, btn_report, btn_info)
info_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_search, btn_report)
report_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_VK, btn_TG, btn_card, btn_address, btn_telephone,
                                                            btn_id, btn_back)
cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_back, btn_cancel)
selections_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_add, btn_delete, btn_back)
yesno_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_yes, btn_no)
o_cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel)

remove_markup = ReplyKeyboardRemove()
