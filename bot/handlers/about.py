from aiogram import Router, types, F
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline.back import back_keyboard

router = Router(name="about")


@router.callback_query(F.data == "about")
async def about_handler(query: types.CallbackQuery) -> None:
    """Information about bot."""
    await query.answer()

    text = _("""
AIKO — Yevropa sifat standartlariga javob beradigan mebel mahsulotlarini ishlab chiqaruvchi sifatida dovrugʻ qozongan brenddir. Kompaniyada 600 dan ortiq xodim mehnat qiladi. Barcha mahsulotlar mashhur jahon brendlarining yuqori sifatli uskunalari yordamida ishlab chiqariladi. AIKO mahsulotlari MDH va qo‘shni mamlakatlar bozorida katta talabga ega.

2020-yilda AIKO ISO 9001-2015 sifat menejmenti xalqaro sertifikatiga sazovor boʻldi, bu kompaniyaga dilerlik tarmog‘ini sezilarli darajada kengaytirish imkoniyatini taqdim etdi. Bugungi kunda AIKO mebellarini nafaqat O‘zbekistonda, balki Qozog‘iston, Rossiya va boshqa ko‘plab mamlakatlarda ham uchratish mumkin. Bundan tashqari, AIKO MDH davlatlarining turli shaharlarida o‘tkazilayotgan xalqaro ko‘rgazmalarda faol ishtirok etib, o‘zining so‘nggi yutuqlari va innovatsiyalarini namoyish etib kelmoqda.

2020-yilda AIKO Toshkentdagi mebel sanoati korxonalari orasida to‘qilgan mebel eksporti bo‘yicha yetakchi o‘rinlardan birini egalladi. Bugungi kunda AIKO mahsulot assortimentida to‘qilgan mebel va uy mebellarining 700 dan ortiq modellari mavjud. Kompaniya 2021 va 2022 yillarda “Yil brendi” nufuzli mukofotiga sazovor boʻlgan, bu esa iste’molchilar va soha mutaxassislarining yuqori ishonch darajasini ifodalaydi.

Kompaniyaning asosiy maqsadi — nafis dizayn, yengillik, soddalik va qulaylikni oʻzida mujassam etgan mebellar yaratish. Biz nafaqat mahsulotlarimiz sifati, balki Yevropa standartlariga javob beradigan estetik ko‘rinishi bilan ham iste’molchilar mehrini qozonganmiz.  AIKOʼning barcha mahsulotlari mustahkam va ishonchli boʻlib, zamonaviy inson uchun mukammal tanlovdir.

Mebelimiz mijozlarimiz xonadonining ajralmas qismiga aylanib, qulaylik va shinamlik baxsh etayotganidan hamisha faxrlanamiz. Mukammallik va innovatsiyalarga doimiy  intilishimiz bizga raqobatchilarimizdan bir qadam oldinda turishga va eng yuqori bozor talablariga javob beruvchi mahsulotlarni taklif qilishga yordam beradi. Ishonchimiz komilki, bu iste’molchilar ishonchini qozonish va sohamiz yetakchisiga aylanishning yagona yo‘li hisoblanadi.

AIKO — shunchaki brend emas, bu sifat va uslub ramzidir. Biz barcha mijozlarimizga bildirilgan ishonch uchun chuqur minnatdorchilik izhor etamiz va ularni mebel olamida yangi va innovatsion yechimlar bilan mamnun etishga tayyormiz. Yutuqlarimiz butun jamoaning mashaqqatli mehnati samarasidir va biz bundan buyon ham yangi marralar va muvaffaqiyatlar sari intilishdan toʻxtamaymiz

Kontakt: +998 55 508 11 88
🌐 aiko.uz
t.me/aiko_uz
www.instagram.com/aiko.uz
📍 Manzil: <a href="https://yandex.uz/maps/-/CDSRjF-P">Yandex</a> | <a href="https://maps.app.goo.gl/WAijBRbMoxUx26Ah7">Google</a>
""")

    await query.message.edit_text(
        text=text,
        reply_markup=back_keyboard()
    )
