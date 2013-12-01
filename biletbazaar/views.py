from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from Events.eventManager import *

def hello(request):
    return HttpResponse("Hola world")
    
def events(request):
    event_list = getAllEvents()
    t = get_template('events.html')
    html = t.render(Context({'event_list':event_list}))
    # insertEvent("konser",'cok hos')
    # insertEventt()

    return HttpResponse(html)