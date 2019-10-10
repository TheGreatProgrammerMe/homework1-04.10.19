from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()

fromtest = {
    'show':0,
    'click':0
}

fromoriginal = {
    'show':0,
    'click':0 
}

def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    froml = str(request.GET.get('from-landing'))
    if froml == 'test':
        fromtest['click'] +=1
    elif froml == 'original':
        fromoriginal['click'] +=1
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    abtestarg = str(request.GET.get('ab-test-arg'))
    if abtestarg == 'test':
        fromtest['show'] +=1
        pagstr = 'landing_alternate.html'
    else:
        fromoriginal['show'] +=1
        pagstr = 'landing.html'
    return render_to_response(pagstr)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    if fromtest['show'] == 0:
        test_con = 'на лендинг не заходили :('
    else:
        test_con = fromtest['click']/fromtest['show']
    if fromoriginal['show'] == 0:
        original_con = 'на лендинг не заходили :('
    else:
        original_con = fromoriginal['click']/fromoriginal['show']
    return render_to_response('stats.html', context={
        'test_conversion': test_con,
        'original_conversion': original_con,
    })
