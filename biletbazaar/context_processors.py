from data.models import *

def autocomplete_tags(request):
    from django.conf import settings
    event_group_alllist = EventGroup.objects.all()
    return {'event_group_alllist': event_group_alllist,'user':request.user}