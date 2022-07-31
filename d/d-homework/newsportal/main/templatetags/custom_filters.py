from django import template
register = template.Library()

from main.models import Post

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    r = d.urlencode()
    print(r)
    return r

@register.simple_tag()
def newscnt(name):
    cnt = Post.objects.filter(pType=name).count()
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
