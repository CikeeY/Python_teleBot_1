import json
import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup as BS


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

bot = telebot.TeleBot('6086228035:AAFDeqPzXntsvxNbTf0O3Kflu_sO7gsaXp0')
#bot = telebot.TeleBot('6425255039:AAFDI3b_merGpbBJK041gHWpBD1CT30WiA0')

urlWeb = 'https://habrahabr.ru'
urlUSD = 'https://www.banki.ru/products/currency/usd/'

cloud = './img/cloud.jpg'
rain = './img/rain.jpg'
clear = './img/sun.png'


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("На сайт")
    btn2 = types.KeyboardButton("Сервис")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Здравствуй, {0.first_name}!\nКонтакт моего разработчика: https://t.me/Pussyeater_228".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "На сайт"):
        markup = types.InlineKeyboardMarkup()
        btn_my_site= types.InlineKeyboardButton(text='habrahabr.ru', url=urlWeb)
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, "На сайт", reply_markup = markup)
    elif(message.text == "Сервис"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Погода")
        btn2 = types.KeyboardButton("Курс валют")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Выбор услуги", reply_markup=markup)
    
    elif(message.text == "Погода"):
        res = requests.get('https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid=9054e8c15a48f4a3b751f6e2b88fc907&units=metric')
        data = json.loads(res.text)
        if data["weather"][0]["main"] == 'Clouds':
            bot.send_photo(message.chat.id, open(cloud, 'rb'))
        elif data["weather"][0]["main"] == 'Rain':
            bot.send_photo(message.chat.id, open(rain, 'rb'))
        elif data["weather"][0]["main"] == 'Clear':
            bot.send_photo(message.chat.id, open(clear, 'rb'))

        bot.send_message(message.chat.id, f'Москва: {data["main"]["temp"]} градусов\n{data["weather"][0]["main"]}')
    
    elif message.text == "Курс валют":
        try:
            page1 = requests.get(urlUSD, headers=headers)
            soup = BS(page1.text, 'lxml')
            cours = soup.find("div", {"class" : "Text__sc-j452t5-0 bCCQWi"}).text
            bot.send_message(message.chat.id, f'Курс доллара: {cours} рублей')
        except Exception as err:
            print(err)
        
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("На сайт")
        button2 = types.KeyboardButton("Сервис")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")

bot.polling(none_stop=True)