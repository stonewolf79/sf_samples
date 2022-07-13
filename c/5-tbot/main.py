debug = True

import os, telebot
from telebot import types as tt
from extensions import *

fname = 'bot_token.cfg'
if not os.path.exists(fname): fname = 'c/'+fname # для моей машины
if not os.path.exists(fname):
    print('Нет файла с токеном')
    os._exit(0)
with open(fname,'r') as f: token = f.readline()

markup = None # кнопки

bot = telebot.TeleBot(token)

def answer(msg, text):
    bot.reply_to(msg, text)

def showHelp(msg:tt.Message):
    text = f'''Доброго времени суток, {msg.from_user.first_name}
    Доступные команды:
    /start и /help - эта справка
    /values - список доступных валют
    /calc валюта1 валюта2 количество - пересчитать количество валюты1 в валюту2. 
    \tесли прямой пары валют нет, будет использован кросс-курс через рубли РФ.
    '''
    answer(msg, text)

def showCurrents(msg:tt.Message):
    Currencies.pull()
    mValues = [f'{e} - {Currencies.short[e]}' for e in Currencies.curr]
    answer(msg, 'Доступные валюты:\n'+'\n'.join(mValues))

@bot.message_handler(commands=['start','help'])
def cmd_help(msg:tt.Message):
    showHelp(msg)

@bot.message_handler(commands=['values'])
def cmd_values(msg:tt.Message):
    showCurrents(msg)

@bot.message_handler(commands=['debug'])
def proc_debug(msg:tt.Message):
    Currencies.pull()
    answer(msg, str(Currencies.data))

@bot.message_handler(commands=['calc'])
def proc_text(msg:tt.Message):
    try:
        params = [p.strip() for p in msg.text.lower().split(' ') if p[0]!='/']
        if len(params)!=3:
            raise APIException('неправильный формат запроса')
        err = '' # ошибки формата обрабатываем сразу все
        if not Currencies.curr: Currencies.pull()
        if params[0] not in Currencies.curr:
            err = f'валюты {params[0]} нет в списке допустимых'
        if params[1] not in Currencies.curr:
            err = f'валюты {params[1]} нет в списке допустимых'
        if not params[2].isnumeric():
            err = f'значение "{params[2]}" не является числом'
        if err: raise APIException(err)
        c1, c2, amount = params[0], params[1], float(params[2])
        err, value = Currencies.get_price(c1, c2, amount)
    except APIException as e:
        answer(msg, f'ошибка в API: {e}')
    except Exception as e:
        answer(msg, f'что-то пошло не так: {e}')
    else:
        answer(msg, f'{amount} {Currencies.short[c1]} = {value:.2f} {Currencies.short[c2]}')
    

print('Бот запущен.')
bot.polling(non_stop=True, timeout=1)
