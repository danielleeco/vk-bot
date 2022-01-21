import os
import logging
import json
from typing import Optional

from dotenv import load_dotenv

from vkbottle import Callback, Keyboard, Text, GroupEventType, GroupTypes, ShowSnackbarEvent, TemplateElement, template_gen
from vkbottle.bot import Bot, Message

from .database import SessionLocal
from . import models

load_dotenv('./.secret')
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)


def make_query(state: str = 'menu', selection: str = None):
    """
    making queries to database
    """
    db = SessionLocal()
    if state == 'menu':
        qquery = [i.section for i in db.query(models.Sections).all()]
    elif state == 'section':
        qquery = [i.product_name for i in db.query(models.Products).filter(models.Products.section == selection).all()]
    elif state == 'item':
        qquery = [
            (i.product_name, i.price, i.weight, i.picture) for i in db.query(models.Products)
            .filter(models.Products.product_name == selection).all()
        ]
    return qquery


rows = make_query(state='menu')

# main keyboard (sections)
MENU_KEYBOARD = Keyboard(inline=False)
for item in rows:
    MENU_KEYBOARD.row().add(Text(f"{item}", {"state": "section"})).get_json()


def build_keyboard(state: str, item: str):
    """
    keyboard from database query
    """
    keyboard_items = Keyboard(inline=False)
    keyboard_items.row().add(Text('Назад', payload={'state': 'menu' if state == 'section' else 'section'}))
    if state == 'section':
        req = make_query(state=state, selection=item)
        for i in req:
            keyboard_items.row().add(Text(f"{i}", {"state": "item"})).get_json()
    return keyboard_items


def new_vktemplate(item: str, state: str = 'item'):
    """
    vk template for presenting the item
    """
    req = make_query(state=state, selection=item)
    name, price, weight, pic = req[0]
    buy = Keyboard().add(Callback(f"Купить за {price} рублей", payload={"state": "buy"})).get_json()
    my_template = template_gen(TemplateElement(
        description=f'Товар: {name}\nВес товара: {weight}',
        photo_id=str(pic), buttons=buy, action={"type": "open_photo"}
    ))
    return my_template


@bot.on.message(text="Привет")
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("Привет, {}! Чтобы продолжить, напиши 'Меню' или 'Начать'".format(users_info[0].first_name))


@bot.on.message(text=["Начать", "Меню"])
async def eat_handler(message: Message, item: Optional[str] = None):
    await message.answer("Отлично! Выбери, что вкусненького тебе приготовить 🤤", keyboard=MENU_KEYBOARD)


@bot.on.message()
async def handler(message: Message) -> str:
    text = message.text
    payload = message.payload
    if payload is None:
        await message.answer("Вот твое меню! Не торопись <3", keyboard=MENU_KEYBOARD)
    else:
        payload = json.loads(payload)
        current_state = payload.get('state', 'menu')
        if current_state == 'menu':
            await message.answer("Вот твое меню! Не торопись <3", keyboard=MENU_KEYBOARD)
        elif current_state == 'section':
            await message.answer(f"Теперь выбери что-нибудь из раздела {text}!", keyboard=build_keyboard(current_state, text))
        elif current_state == 'item':
            await message.answer(f"{text}! Отличный выбор 🤤", template=new_vktemplate(text))


@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def handle_message_event(event: GroupTypes.MessageEvent):

    await bot.api.messages.send_message_event_answer(
        event_id=event.object.event_id,
        user_id=event.object.user_id,
        peer_id=event.object.peer_id,
        event_data=ShowSnackbarEvent(text="Спасибо за покупку! Денюшка скоро спишется с твоей карты 🤗").json(),
    )

logging.basicConfig(level=logging.DEBUG)
