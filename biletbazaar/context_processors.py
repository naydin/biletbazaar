from data.models import *

def autocomplete_tags(request):
    from django.conf import settings
    
    selected_category = ''
    try:
        selected_category = request.GET['category']
    except Exception as e:
        selected_category = ''

    color = ''
    if selected_category == 'muzik':
        color = '#37a0ba'
    elif selected_category == 'spor':
        color = '#afc52d'
    elif selected_category == 'sahne':
        color = '#f8c600'
    event_group_alllist = EventGroup.objects.all()
    return {'event_group_alllist': event_group_alllist,'user':request.user,'anasayfa_color':color}