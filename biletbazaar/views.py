# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context,loader
from data.eventManager import *
from data.models import *
from django.shortcuts import render
from forms import *
from modelForms import *
from django.db.models import Max
from static_data import *

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

selected_city_name_field = "selected_city_name"

def hello(request):
    return HttpResponse("Hola world")

def reset_data(request):
    try:
        reset_static_data()
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))

    return HttpResponse("Reset Successful.")

def admin_panel(request):
    eventGroupModelForm = EventGroupModelForm()
    eventModelForm = EventModelForm()
    ticketModelForm = TicketModelForm()
    userModelForm = UserModelForm()
    landingUserModelForm = LandingUserModelForm()
    cityModelForm = CityModelForm()
    
    if request.method == 'POST':
        if 'eventGroupModelForm' in request.POST:
            form = EventGroupModelForm(request.POST)
        if 'eventModelForm' in request.POST:
            form = EventModelForm(request.POST)
        if 'ticketModelForm' in request.POST:
            form = TicketModelForm(request.POST)
        if 'userModelForm' in request.POST:
            form = UserModelForm(request.POST)
        if 'landingUserModelForm' in request.POST:
            form = LandingUserModelForm(request.POST)
        if 'cityModelForm' in request.POST:
            form = CityModelForm(request.POST)
            
        if form.is_valid():
            form.save(commit=True)
            # cd = form.cleaned_data
            # send_mail(
            #     cd['subject'],
            #     cd['message'],
            #     cd.get('email', 'noreply@example.com'),
            #     ['siteowner@example.com'],
            # )
            return HttpResponse("Success")
        else:
            if 'eventGroupModelForm' in request.POST:
                eventGroupModelForm = form
            if 'eventModelForm' in request.POST:
                eventModelForm = form
            if 'ticketModelForm' in request.POST:
                ticketModelForm = form
            if 'userModelForm' in request.POST:
                userModelForm = form
            if 'landingUserModelForm' in request.POST:
                landingUserModelForm = form
            if 'cityModelForm' in request.POST:
                cityModelForm = form
                
    return render(request, 'admin_panel.html', {'eventGroupModelForm': eventGroupModelForm,'eventModelForm':eventModelForm,'ticketModelForm':ticketModelForm,'userModelForm':userModelForm,'landingUserModelForm':landingUserModelForm,'cityModelForm':cityModelForm})
    

def landing(request):
    clientError = u""
    if request.method == 'POST':
        reqEmail = request.POST['email']

        try:
            if LandingUser.objects.get(email=reqEmail).email == reqEmail:
                clientError = u"Bu e-mail zaten mevcut."
                return render(request,'landing_page.html',{'base':'/static/','error':clientError})
        except LandingUser.DoesNotExist:
            pass

        try:
            validate_email(reqEmail)
        except ValidationError:
            clientError = u"Lutfen Gecerli bir e-mail adresi girin."
            return render(request,'landing_page.html',{'base':'/static/','error':clientError})

        user = LandingUser()
        user.email = reqEmail
        user.save()
        clientError = u"E-mail adresiniz sistemize kaydedildi."
        
        send_maill(reqEmail)
        
    return render(request,'landing_page.html',{'base':'/static/','error':clientError})
    


def bilet_ilan(request):
    selected_city_name = u''
    if request.session[selected_city_name_field]:
        selected_city_name = request.session[selected_city_name_field]
    
    print "cityname=" + selected_city_name
    
    event_list = []
    if request.method == 'POST':
        if request.POST['search_event_group_name']:
            search_event_group_name = request.POST['search_event_group_name']
            event_list = Event.objects.filter(eventGroup__name__icontains=search_event_group_name,city__name__contains=selected_city_name)
            
    event_group_list = EventGroup.objects.all()
    print len(event_list)
    
    return render(request,'bilet_ilan.html',{'base':'/static/','event_group_list':event_group_list,'event_list':event_list})


def anasayfa(request):
    # max_sale_count = EventGroup.objects.all().aggregate(Max('saleCount'))['saleCount__max']
    # event_group_list = EventGroup.objects.filter(saleCount = max_sale_count)
    # event_group = event_group_list[0]
    # event_list = event_group.event_set.all()
    
    selected_city_name = u''
    
    #check if a city is selected previously and stored in a cookie
    if selected_city_name_field in request.COOKIES:
        selected_city_name = ''.join((request.COOKIES[selected_city_name_field])).decode('utf-8').strip()
    
    #if a city is posted take that as selected city
    try:
        selected_city_name = request.POST['city_select']
    except Exception as e:
        # print '%s (%s)' % (e.message, type(e))
        pass
    
    #validate selected city,if valid save it to session
    try:
        City.objects.get(name=selected_city_name)
        request.session[selected_city_name_field] = selected_city_name
    except Exception as e:
        selected_city_name = ""
    
    
    #query the required lists
    event_group_list = EventGroup.objects.all().order_by('-saleCount')[0:5]
    event_list = Event.objects.filter(city__name__contains=selected_city_name).order_by('date')[0:10]
    ticket_list = Ticket.objects.filter(event__city__name__contains=selected_city_name).order_by('price')[0:5]
    city_list = City.objects.all()

    #prepare the response
    response = render(request,'main_page.html',{'base':'/static/','event_list':event_list,'event_group_list':event_group_list,
    'ticket_list':ticket_list,"city_list":city_list,'selected_city_name':selected_city_name,'city_name_all_cities':u"Tüm Türkiye"})

    #include selected city in the cookie
    print u''.join((selected_city_name)).encode('utf-8').strip()
    response.set_cookie(selected_city_name_field,u''.join((selected_city_name)).encode('utf-8').strip())
        
    return response

def send_maill(email):
    subject, from_email, to = 'Bilet Bosta\'ya Hosgeldiniz', 'info@biletbosta.com',email
    text_content = ''
    c = Context({'ig_url':'http://www.biletbosta.com/static/bilet-bosta-reklam.png'})
    t = loader.get_template('mail_template.html')
    html_content = t.render(c)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

