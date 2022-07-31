from datetime import datetime
from django import template
register = template.Library()

from main.models import Post

@register.filter()
def newscnt(val):
    cnt = 0
    for p in val:
        if p.pType=='N': cnt += 1
    return cnt

badWords = 'редиска,сволочь'.split(',')
@register.filter()
def censor(text:str):
    ''' убирает запрещённые слова '''
    ltext = text.lower()
    for word in badWords:
        wlen = len(word)
        while(True):
            index = ltext.find(word)
            if index==-1: break
            ltext = ltext[:index]+('*'*(wlen))+ltext[index+wlen:]
            text = text[:index+1]+('*'*(wlen-1))+text[index+wlen:]
    return text
