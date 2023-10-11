import os
import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='6266381981:AAGZMyu1mONTsJVTocmWuoI-RZWfK1LBB3I')
dp = Dispatcher(bot)


# Вызов функции start_command и вывод сообщения при получении команды /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды")


@dp.message_handler()
async def get_weather(message: types.Message):  # Содержит информацию отправленную пользователем
    try:
        city_name = message.text  # присваиваем переменной название города кототрый ввел пользователь

        # Производим запрос на сайт прогноз погоды с помощью функции requests.get()
        response = requests.get(
            # Получаем запрос API погоды. вставляем переменую в запрос для получения данных о погоде
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&lang=ru&units=metric&appid=3d2245384af4b37b2fdd68ca8d0baa1d")
        data = response.json()  # Метод который преобразует ответ от сервера в формате JSON в объект python и помещаем ее в переменую data
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        # продолжительность дня
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"Погода в городе: {city}\nТемпература: {cur_temp} °C \n"
                            f"Влажность: {humidity}%\nДавление: {(pressure / 1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
                            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                            f"Хорошего дня!"
                            )
    except:
        await message.reply("Проверьте название города!")


if __name__ == "__main__":
    executor.start_polling(dp)
