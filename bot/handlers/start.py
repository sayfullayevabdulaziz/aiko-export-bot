from aiogram import F, Bot, Router, types
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.menu import main_keyboard
from bot.keyboards.inline.language import LanguageCallback, language_keyboard
# from bot.services.analytics import analytics
from sqlalchemy.ext.asyncio import AsyncSession
from bot.keyboards.inline.perm import permission_keyboard
from bot.keyboards.reply.get_phone_kbd import register_btn
from bot.services.users import get_admins, user_exists, add_user, set_language_code, set_phone, get_user
from bot.states.register_form import RegisterFormState

router = Router(name="start")


# @analytics.track_event("Sign Up")
@router.message(CommandStart())
async def start_handler(message: types.Message, session: AsyncSession, state: FSMContext) -> None:
    """Welcome message."""
    user = await get_user(session=session, user_id=message.from_user.id)

    if user is None:
        await message.answer(
            text='Assalomu Alaykum! Kerakli tilni tanlang\n'
                 'Здравствуйте! Выберите необходимый язык',
            reply_markup=language_keyboard()
        )
    elif user.phone is None:
        await state.set_state(RegisterFormState.number)
        await message.answer(text=_("Iltimos, telefon raqamingizni yuboring"),
                             reply_markup=await register_btn())
    else:
        await message.answer(_("Asosiy menu"), reply_markup=main_keyboard(),)


@router.callback_query(LanguageCallback.filter())
async def user_save_from_fab(query: types.CallbackQuery, callback_data: LanguageCallback, session: AsyncSession, state: FSMContext):
    """
        User create or update language_code 
    """
    language_code = callback_data.language_code
    user_exist = await user_exists(session=session, user_id=query.from_user.id)

    if not user_exist:
        await add_user(session=session, user=query.from_user, language_code=language_code)
        await state.set_state(RegisterFormState.number)
        await query.message.answer(text=_("Iltimos, telefon raqamingizni yuboring", locale=language_code),
                                   reply_markup=await register_btn(locale=language_code))

        # await query.message.edit_text(
        #     text=_("Asosiy menu", locale=language_code),
        #     reply_markup=main_keyboard(locale=language_code),
        # )
    else:
        await set_language_code(session=session, user_id=query.from_user.id, language_code=language_code)

        await query.message.edit_text(
            text=_("Asosiy menu", locale=language_code),
            reply_markup=main_keyboard(locale=language_code),
        )


@router.message(F.contact, RegisterFormState.number)
async def contact_handler(message: types.Message, session: AsyncSession, state: FSMContext, bot: Bot) -> None:
    """User phone."""
    phone = message.contact.phone_number

    if not phone.startswith("+"):
        phone = "+" + phone

    await state.clear()

    await set_phone(session=session, user_id=message.from_user.id, phone=phone)
    admins = await get_admins(session=session)
    
    for admin in admins:
        text = _("Yangi foydalanuvchi sizni ruxsatingizni kutyabdi.\n\n")
        text += _("ID: {}\n").format(message.from_user.id)
        text += _("Ismi: {}\n").format(message.from_user.mention_html())
        text += _("username: @{}\n").format(message.from_user.username)
        text += _("Telefon raqami: {}").format(phone)

        await bot.send_message(
            chat_id=admin.user_id, 
            text=text, 
            reply_markup=await permission_keyboard(user_id=message.from_user.id)
        )
    

    await message.answer(_("Telefon raqamingiz qabul qilindi. Admin ruxsatini kuting."), reply_markup=types.ReplyKeyboardRemove())


@router.message(RegisterFormState.number)
async def process_unknown_write_bots(message: types.Message) -> None:
    await message.reply(_("Iltimos, telefon raqamingizni yuboring"))