from datetime import datetime, timedelta
import requests, json
import lxml.html as html
from telebot import types as tt

class APIException(BaseException):
    pass

class Currencies:

    lastUpdate = None # последнее обновление
    curr = None # валюты
    rub = 'rub'
    data = {} # данные курсов
    updTime = timedelta(minutes=10) # минимальный интервал обновления

    @staticmethod
    def pull():
        '''получает курсы валют'''
        now = datetime.now()
        if Currencies.lastUpdate and now-Currencies.lastUpdate<Currencies.updTime: return Currencies.data
        Currencies.lastUpdate = now
        # курсы валют 
        # xml  Центробанк   https://www.cbr.ru/scripts/XML_daily.asp
        # json РБК          https://quote.ru/v5/ajax/index
        text = Currencies.getResource('https://quote.ru/v5/ajax/index', 'Запрос курсов валют')
        jdata = json.loads(text)
        tree = html.document_fromstring(jdata['currency'])
        # indices__name
        # <span class="indices__sum">\n\n  $1,008  \n</span>
        names = tree.xpath('//span[@class="indices__name"]')
        vals = tree.xpath('//span[@class="indices__sum"]')
        data = Currencies.data
        for name, val in zip(names, vals):
            sv = val.text.strip()[1:].replace(',','.')
            if not sv: continue
            n = name.text.lower().strip()
            nFrom, nTo = n.split('/')
            if not nFrom in data: data[nFrom] = {}
            v = float(sv)
            data[nFrom][nTo] = v

        Currencies.short = Currencies.getShort()
        Currencies.getCurr()

        return data
    
    @staticmethod
    def getResource(url:str, name:str):
        '''возвращает страницу с замером времени или None'''
        tstart = datetime.now()
        print(f'{name} ... ', end='')
        try:
            text = requests.get(url).text
        except:
            return None
        t = datetime.now()-tstart
        print(f'выполнен за {t}')
        return text

    @staticmethod
    def getShort():
        url = 'https://classifikators.ru/okv'
        
        text = Currencies.getResource(url, 'Запрос классификатора')
        if text is None:
            print(f'Ошибка получения страницы {url}')
            return
        tree = html.document_fromstring(text)
        enames = tree.xpath('//*[@id="codes"]/div[1]/table/tbody/tr')
        short = {e.find('td[3]').text.lower(): e.find('td[4]').text for e in enames}
        return short

    @staticmethod
    def getCurr():
        '''список валют'''
        if Currencies.curr: return Currencies.curr
        if not Currencies.data: Currencies.pull()
        mCurr = []
        for f, t in Currencies.data.items():
            mCurr.append(f)
            mCurr += t
        Currencies.curr = set(mCurr)

    @staticmethod
    def get_price(base, quote, amount=1, recurse=True):
        '''пересчёт курса'''
        cls = Currencies
        rub = cls.rub
        if not cls.data: cls.pull()
        if base in cls.data and quote in cls.data[base]:
            return None, amount*cls.data[base][quote] # прямой курс
        elif quote in cls.data and base in cls.data[quote]:
            return None, amount/cls.data[quote][base] # обратный курс
        # прямого курса нет, проверяем курсы валют к доллару
        if base in cls.data and cls.rub in cls.data[base] and rub in cls.data[quote]:
            return None, amount*cls.data[base][rub]/cls.data[quote][rub]
        # прямого кросс-курса нет, проверяем обратный кросс
        if recurse: 
            err, value = cls.get_price(quote, base, recurse=False)
            if err is None: return None, amount/value
        # ничего не нашли :'(
        return f'валюту "{cls.short[base]}" невозможно преобразовать 😢', None 
            
