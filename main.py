from PIL import Image, ImageFont, ImageDraw
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '7642306739:AAGsD41ZOrf5LLAh3J8L5sthU0ZWCrBvG8s'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    fullname = State()
    phone = State()
    email = State()
    site = State()
    address = State()
    company = State()
    job = State() 
    finish = State()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await UserState.fullname.set()
    await message.reply("Assalomu aleykum! Ism-Familyangizni kiriting:")

@dp.message_handler(state=UserState.fullname)
async def get_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await message.answer("Telefon raqamingizni kiriting:")
    await UserState.next()

@dp.message_handler(state=UserState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await message.answer("Elektron pochtangizni kiriting:")
    await UserState.next()

@dp.message_handler(state=UserState.email)
async def get_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await message.answer("Saytingizi kiriting:")
    await UserState.next()

@dp.message_handler(state=UserState.site)
async def get_site(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['site'] = message.text
    await message.answer("Addressingizni kiriting:")
    await UserState.next()

@dp.message_handler(state=UserState.address)
async def get_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await message.answer("Kompaniya nomini kiriting:")
    await UserState.next()

@dp.message_handler(state=UserState.company)
async def get_company(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['company'] = message.text
    await message.answer("Kasbingizni kiriting:")
    await UserState.next()

@dp.message_handler(state=UserState.job)
async def get_job(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['job'] = message.text
    await message.answer("Ma'lumotlar qabul qilindi. Vizitka tayyorlanmoqda...")

    # Foydalanuvchi ma'lumotlarini olish
    fullname = data['fullname']
    phone = data['phone']
    email = data['email']
    site = data['site']
    address = data['address']
    company = data['company']
    job = data['job']

    # Vizitka yaratish funksiyasini chaqirish
    filename = create_fullname_card(fullname, phone, email, site, address)
    filename1 = create_company_card(company, job)

    # Tayyorlangan vizitkani foydalanuvchiga jo‘natish
    with open(filename, 'rb') as photo:
        await bot.send_photo(message.chat.id, photo)
    with open(filename1, 'rb') as photo1:
        await bot.send_photo(message.chat.id, photo1, caption="Mana sizning vizitka.")

    await state.finish()

def create_fullname_card(fullname, phone, email, site, address):
    fg = Image.open(r"fg.png")  # fg rasmni ochish

    draw_fg = ImageDraw.Draw(fg)
    draw_fg.text((125, 120), fullname.title(), font=ImageFont.truetype("MuseoSansCyrl.otf", 70), fill=(194, 149, 61))
    draw_fg.text((170, 268), phone, font=ImageFont.truetype("MuseoSansCyrl.otf", 35), fill=(194, 149, 61))
    draw_fg.text((170, 325), email, font=ImageFont.truetype("MuseoSansCyrl.otf", 35), fill=(194, 149, 61))
    draw_fg.text((170, 380), site, font=ImageFont.truetype("MuseoSansCyrl.otf", 35), fill=(194, 149, 61))
    draw_fg.text((170, 445), address, font=ImageFont.truetype("MuseoSansCyrl.otf", 35), fill=(194, 149, 61))

    filename = f"{fullname}_card.png"
    fg.save(filename)
    return filename

def create_company_card(company, job):
    bg = Image.open(r"bg.png")  # bg rasmni ochish

    draw_bg = ImageDraw.Draw(bg)
    draw_bg.text((260, 340), company, font=ImageFont.truetype("MuseoSansCyrl.otf", 80), fill=(194, 149, 61))
    draw_bg.text((370, 430), job.title(), font=ImageFont.truetype("MuseoSansCyrl.otf", 65), fill=(194, 149, 61))

    filename1 = f"{company}_card.png"
    bg.save(filename1)
    return filename1

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)