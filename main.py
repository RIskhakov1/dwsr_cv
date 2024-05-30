import asyncio
import logging
import sys
import numpy as np

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import tensorflow as tf
# from keras.src.legacy.preprocessing import image
from PIL import Image



TOKEN = "6718404187:AAGoEXRIbm0u5uJ4l16nZyUPCcjU0qxDAaQ"

model = tf.keras.models.load_model('tiger_wolf_model.h5')

def preprocess_images(path):
    img = Image.open(path).convert('RGB')
    img = img.resize((256, 256))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    return img_array

def test(img_path):
    img = preprocess_images(img_path)
    prediction = model.predict(img)

    predicted_class_index = int(np.round(prediction))
    class_labels = ['tiger', 'white_wolf']
    predicted_class_label = class_labels[predicted_class_index]
    if predicted_class_label == 'tiger':
        return 1
    else:
        return 0

dp = Dispatcher()
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Ну привет, {html.bold(message.from_user.full_name)}!")

@dp.message(F.photo)
async def photo_handler(message: Message) -> None:
    await message.bot.download(file=message.photo[-1].file_id,
                               destination='/home/rinat/oirs/bot/received_images/test.jpg')

    if test('/home/rinat/oirs/bot/received_images/test.jpg') == 1:
        await message.answer(f"Tiger")
    else:
        await message.answer(f"Wolf")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        await message.answer("Nice try!")
    except TypeError:
        await message.answer("Nice try!")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())