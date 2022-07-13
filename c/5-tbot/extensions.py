from datetime import datetime, timedelta
import requests, json
import lxml.html as html

class APIException(BaseException):
    pass

class Currencies:

    lastUpdate = None # последнее обновление
    curr = None # валюты
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
        text = requests.get('https://quote.ru/v5/ajax/index').content
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
    def getResource(url, name):
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
    def get_price(base, qoute, amount=1):
        '''пересчёт курса'''
        if not Currencies.data: Currencies.pull()
        if not base in Currencies.data:
            err = f'валюту "{base}" невозможно преобразовать' # если вдруг произошло странное
        elif not qoute in Currencies.data[base]:
            # прямого курса нет, проверяем вторую на курс с долларом
            if qoute in Currencies.data['usd']:
                value = 
