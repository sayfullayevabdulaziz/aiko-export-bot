from aiogram import types, Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from bot.filters.chat_type import ChatTypeFilter

group_router = Router()


@group_router.message(Command("me"), StateFilter(None), ChatTypeFilter(chat_type=['group', 'supergroup']))
async def about_group(message: types.Message):
    text = f"Username: {message.chat.username}\n"
    text += f"Title: {message.chat.title}\n"
    text += f"ID: {message.chat.id}"
    await message.answer(text)