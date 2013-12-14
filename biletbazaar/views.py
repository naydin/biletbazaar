from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from data.eventManager import *
from data.models import *
from django.shortcuts import render
from forms import *

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def hello(request):
    return HttpResponse("Hola world")

def event_groups(request):
    if request.method == 'POST':
        form = EventGroupForm(request.POST)
        if form.is_valid():
            # cleaned_data = form.cleaned_data
#             cleaned_data.save()
            form.save()
            return HttpResponse("Thanks")
        else:
            return HttpResponse("Error")
    else:
        form = EventGroupForm()
    return render(request,'event_group_form.html',{'form':form})

def landing(request):
    if request.method == 'POST':
        reqEmail = request.POST['email']
        try:
            if LandingUser.objects.get(email=reqEmail).email == reqEmail:
                return HttpResponse("Bu mail var panpa")
        except LandingUser.DoesNotExist:
            pass

        try:
            validate_email(reqEmail)
        except ValidationError:
            return HttpResponse("Adam gibi mail gir lan")

        user = LandingUser()
        user.email = reqEmail
        # user.save()

    return render(request,'landing_page.html',{'base':'/static/'})

# def events(request):
#     event_list = getAllEvents()
#     t = get_template('events.html')
#     html = t.render(Context({'event_list':event_list}))
#     # insertEvent("konser",'cok hos')
#     # insertEventt()
# 
#     return HttpResponse(html)

