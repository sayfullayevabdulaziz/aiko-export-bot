from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class LanguageCallback(CallbackData, prefix="language"):
    language_code: str


languages = {
    "ru": "🇷🇺 Русский",
    "uz": "🇺🇿 O'zbek"
}


def language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for language_code, language_name in languages.items():
        builder.row(
            InlineKeyboardButton(
                text=language_name,
                callback_data=LanguageCallback(language_code=language_code).pack()
            ))
    return builder.as_markup()