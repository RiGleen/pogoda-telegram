import telebot
from telebot.apihelper import send_message
import config
import sqlite3
import random
import time
import requests
from datetime import date
today = date.today()
from time import sleep







def get_wind_direction(deg):
    l = ['С ','СВ',' В','ЮВ','Ю ','ЮЗ',' З','СЗ']
    for i in range(0,8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res


from peewee import *
db = SqliteDatabase('database10.db')
class User(Model):
    user_id = TextField()
    city = IntegerField(default=0)
    start = IntegerField(default=0)
    age = IntegerField(default=0)


    class Meta:
        database = db
        db_table = 'users'
User.create_table()
def does_it_exist(model, instance):
    exits = model.select().where(model.user_id == instance)
    if not bool(exits):
        return True
    else:
        return False

def reg_DB(uid):
    if not does_it_exist(User, uid):
        user = User.get(User.user_id == uid)
        user.save()

    else:
        print('I')
        usersDB = User(user_id = uid)
        usersDB.save()


bot = telebot.TeleBot(config.TOKEN)



@bot.message_handler(commands=['start'])
def start_message(message):
    reg_DB(message.from_user.id)
    user = User.get(User.user_id == message.from_user.id)
    start = User.get(User.user_id == message.from_user.id).start
    if start <= 0:
        user.start +=1;
        user.save()
        bot.send_message(message.chat.id, 'Регистрирую в системе...')
        bot.send_message(message.chat.id,  message.from_user.id )
        bot.send_message(message.chat.id, 'Привет, я твой ассистент прогноза погоды ;)')
        bot.send_message(message.chat.id, 'У меня есть команда /city, она показывает список городов.')
        bot.send_message(message.chat.id, 'Скоро я сделаю возможность при регистрации указать свой город, и писать "Погода')
    else:
        bot.send_message(message.chat.id, 'Проверяю в системе...')
        bot.send_message(message.chat.id, message.from_user.id)
        bot.send_message(message.chat.id, 'Я рад тебя снова видеть, я твой ассистент прогноза погоды - если ты забыл ;)')
        bot.send_message(message.chat.id, 'У меня есть команда /city, она показывает список городов.')



@bot.message_handler(commands=['reg'])
def reg_city_message(message):
    user = User.get(User.user_id == message.from_user.id)
    useid = User.get(User.user_id == message.from_user.id).user_id
    if user.id >0:
        bot.send_message(message.chat.id, f'Ты уже зарегистрирован: {useid}')
        bot.send_message(message.chat.id, 'Для окончания регистрации, давай введём твой город')
        bot.send_message(message.chat.id, 'Чтобы добавить, введи (/city) пример: ("/Moscow", список названий в /city')

    else:
        reg_DB()
        user.save()
        return



@bot.message_handler(commands=['Moscow'])
def reg_city1_message(message):
        user = User.get(User.user_id == message.from_user.id)
        useid = User.get(User.user_id == message.from_user.id).user_id
        city = User.get(User.user_id == message.from_user.id).city
        user.city = 524901
        user.save()
        bot.send_message(message.chat.id, f'Поздравляю {useid} ты прошёл регистрацию, теперь твой основной город Москва!')
        bot.send_message(message.chat.id, 'Чтобы поменять свой город пропиши /reset')
        bot.send_message(message.chat.id, 'Тебе доступны команды (Погода на завтра) (Погода) ')

@bot.message_handler(commands=['Saint-Petersburg'])
def reg_city2_message(message):
        user = User.get(User.user_id == message.from_user.id)
        user_id = User.get(User.user_id == message.from_user.id).user_id
        city = User.get(User.user_id == message.from_user.id).city
        user.city = 519690
        user.save()
        bot.send_message(message.chat.id, f'Поздравляю {user_id} ты прошёл регистрацию, теперь твой основной город Санкт-Петербург!')
        bot.send_message(message.chat.id, 'Чтобы поменять свой город пропиши /reset')
        bot.send_message(message.chat.id, 'Тебе доступны команды (Погода на завтра) (Погода) ')

@bot.message_handler(commands=['reset'])
def reset_message(message):
        user = User.get(User.user_id == message.from_user.id)
        user_id = User.get(User.user_id == message.from_user.id).user_id
        city = User.get(User.user_id == message.from_user.id).city
        user.city = 0
        user.save()
        bot.send_message(message.chat.id, f'Данные о городе сброшены {user_id}')
        bot.send_message(message.chat.id, 'Чтобы поставить новый город пропиши "/название" города. Правильная форма на английском /city')



@bot.message_handler(commands=['city'])
def city_message(message):
    bot.send_message(message.chat.id, 'Города:')
    bot.send_message(message.chat.id, 'Москва - (Москва) (Moscow)')
    bot.send_message(message.chat.id, 'Санкт-Петербург - (Санкт-Петербург),(Питер),(Saint-Petersburg) ')

@bot.message_handler(func=lambda message: True)
def message_variant_2(message):
    
    if 'Питер' in message.text:
        city_id = 519690
        appid = "cd99067ce8aab00a0bce71b828aeb51e"
        bot.send_message(message.chat.id,'Санкт-Петербург')
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            print("conditions:", data['weather'][0]['description'])
            ab=data['weather'][0]['description']
            print("temp:", data['main']['temp'])
            ac=data['main']['temp']
            print("temp_min:", data['main']['temp_min'])
            av=data['main']['temp_min']
            print("temp_max:", data['main']['temp_max'])
            ad=data['main']['temp_max']
            print("data:", data)
            bot.send_message(message.chat.id,ab)
            bot.send_message(message.chat.id, f'Температура: {ac} С°')
            bot.send_message(message.chat.id,f'Минимальная Температура: {av} С°')
            bot.send_message(message.chat.id,f'Максимальная Температура: {ad} С°')
        except Exception as e:
                    bot.send_message("Exception (weather):", e)
                    pass
     
    if 'Санкт-Петербург' in message.text:
        city_id = 519690
        appid = "cd99067ce8aab00a0bce71b828aeb51e"
        bot.send_message(message.chat.id,'Санкт-Петербург')
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            print("conditions:", data['weather'][0]['description'])
            ab=data['weather'][0]['description']
            print("temp:", data['main']['temp'])
            ac=data['main']['temp']
            print("temp_min:", data['main']['temp_min'])
            av=data['main']['temp_min']
            print("temp_max:", data['main']['temp_max'])
            ad=data['main']['temp_max']
            print("data:", data)
            bot.send_message(message.chat.id,ab)
            bot.send_message(message.chat.id, f'Температура: {ac} С°')
            bot.send_message(message.chat.id,f'Минимальная Температура: {av} С°')
            bot.send_message(message.chat.id,f'Максимальная Температура: {ad} С°')
        except Exception as e:
                    bot.send_message("Exception (weather):", e)
                    pass
    
    if 'Москва' in message.text:
        city_id=524901
        appid = "cd99067ce8aab00a0bce71b828aeb51e"
        bot.send_message(message.chat.id,'Москва:')
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            print("conditions:", data['weather'][0]['description'])
            ab=data['weather'][0]['description']
            print("temp:", data['main']['temp'])
            ac=data['main']['temp']
            print("temp_min:", data['main']['temp_min'])
            av=data['main']['temp_min']
            print("temp_max:", data['main']['temp_max'])
            ad=data['main']['temp_max']
            print("data:", data)
            bot.send_message(message.chat.id,ab)
            bot.send_message(message.chat.id, f'Температура: {ac} С°')
            bot.send_message(message.chat.id,f'Минимальная Температура: {av} С°')
            bot.send_message(message.chat.id,f'Максимальная Температура: {ad} С°')

        except Exception as e:
            bot.send_message("Exception (weather):", e)
            pass
    if 'Moscow' in message.text:
        city_id=524901
        appid = "cd99067ce8aab00a0bce71b828aeb51e"
        bot.send_message(message.chat.id,'Москва:')
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            print("conditions:", data['weather'][0]['description'])
            ab=data['weather'][0]['description']
            print("temp:", data['main']['temp'])
            ac=data['main']['temp']
            print("temp_min:", data['main']['temp_min'])
            av=data['main']['temp_min']
            print("temp_max:", data['main']['temp_max'])
            ad=data['main']['temp_max']
            print("data:", data)
            bot.send_message(message.chat.id,ab)
            bot.send_message(message.chat.id, f'Температура: {ac} С°')
            bot.send_message(message.chat.id,f'Минимальная Температура: {av} С°')
            bot.send_message(message.chat.id,f'Максимальная Температура: {ad} С°')

        except Exception as e:
            bot.send_message("Exception (weather):", e)
            pass

    if 'Погода' in message.text:
        user = User.get(User.user_id == message.from_user.id)
        city = User.get(User.user_id == message.from_user.id).city
        if user.city == 524901:
            city_id = 524901
            appid = "cd99067ce8aab00a0bce71b828aeb51e"
            bot.send_message(message.chat.id, 'Москва:')
            try:
                res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                   params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
                data = res.json()
                print("conditions:", data['weather'][0]['description'])
                ab = data['weather'][0]['description']
                print("temp:", data['main']['temp'])
                ac = data['main']['temp']
                print("temp_min:", data['main']['temp_min'])
                av = data['main']['temp_min']
                print("temp_max:", data['main']['temp_max'])
                ad = data['main']['temp_max']
                print("data:", data)
                bot.send_message(message.chat.id, ab)
                bot.send_message(message.chat.id, f'Температура: {ac} С°')
                bot.send_message(message.chat.id, f'Минимальная Температура: {av} С°')
                bot.send_message(message.chat.id, f'Максимальная Температура: {ad} С°')

            except Exception as e:
                bot.send_message("Exception (weather):", e)
                pass

        else:
            bot.send_message(message.chat.id, 'Вы не прошли регистрацию города,подробнее /reg')
        if user.city == 519690:
            city_id = 519690
            appid = "cd99067ce8aab00a0bce71b828aeb51e"
            bot.send_message(message.chat.id, 'Санкт-Петербург')
            try:
                res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                   params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
                data = res.json()
                print("conditions:", data['weather'][0]['description'])
                ab = data['weather'][0]['description']
                print("temp:", data['main']['temp'])
                ac = data['main']['temp']
                print("temp_min:", data['main']['temp_min'])
                av = data['main']['temp_min']
                print("temp_max:", data['main']['temp_max'])
                ad = data['main']['temp_max']
                print("data:", data)
                bot.send_message(message.chat.id, ab)
                bot.send_message(message.chat.id, f'Температура: {ac} С°')
                bot.send_message(message.chat.id, f'Минимальная Температура: {av} С°')
                bot.send_message(message.chat.id, f'Максимальная Температура: {ad} С°')
            except Exception as e:
                bot.send_message("Exception (weather):", e)
                pass
        else:
            bot.send_message(message.chat.id, 'Вы не прошли регистрацию города,подробнее /reg')
    if 'репка' in message.text:
        a = 5
        b = 1
        c = 0
        bot.send_message(message.chat.id, 'Семенков 10 Б ;) ')
        while c < a:
                c = c + b
                print(c)
                if c == 1:
                    bot.send_message(message.chat.id, f'Дед тянет за репку не вытянет, позвал дед бабку {c}')

                if c == 2:
                    bot.send_message(message.chat.id, f'Тянет бабка с дедом репку, вытянуть не могут, позвали внучку {c}')
                if c == 3:
                    bot.send_message(message.chat.id, f'Тянет бабка,внучка, дед репку, вытянуть не могут, позвали жучку {c}')
                if c == 4:
                    bot.send_message(message.chat.id, f'Тянет бабка,внучка,жучка дед репку,вытянуть не могут, позвали мышку. {c}')
                if c == 5:
                    bot.send_message(message.chat.id, f'Тянут репку: бабка,внучка,жучка,дед и мышка {c}')
        bot.send_message(message.chat.id, f'Репку вытянули, количество повторов {c}')
        pass

            

print(today)
print('bot_enable')
bot.polling(none_stop=True)