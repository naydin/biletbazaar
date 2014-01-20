# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context,loader
from data.eventManager import *
from data.models import *
from django.shortcuts import render,redirect
from forms import *
from modelForms import *
from django.db.models import Max
from static_data import *

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

import re

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


#sell

def bilet_ilan(request):
    selected_city_name = u''
    try:
        selected_city_name = request.session[selected_city_name_field]
    except Exception as e:
        selected_city_name = u''
    
    event_list = []
    if request.method == 'POST':
        if request.POST['search_event_group_name']:
            search_event_group_name = request.POST['search_event_group_name']
            event_list = Event.objects.filter(eventGroup__name__icontains=search_event_group_name,city__name__icontains=selected_city_name)
            
    event_group_list = EventGroup.objects.all()
    
    return render(request,'sell/bilet_ilan.html',{'base':'/static/','event_group_list':event_group_list,'event_list':event_list})

valid_ticket_count_range = range(1,7)

def bilet_detaylari(request):
    if request.method == 'POST':
        try:        
            event_id = request.session['sell_event_id']
            event = Event.objects.get(id=event_id)
            
            ticket_count = ''
            seat_category = ''
            seat_row = ''
            seat_number = ''
            ticket_count_error = ''
            seat_category_error = ''
            seat_row_error = ''
            seat_number_error = ''
            
            try:
                ticket_count = request.POST['ticket_count']
                if int(ticket_count) not in valid_ticket_count_range:
                    raise Exception('')
            except Exception as e:
                ticket_count_error = u'Lütfen geçerli bir bilet sayısı girin.'
                
            try:
                seat_category = request.POST['seat_category']
                if not event.isSeatCategoryValid(seat_category):
                    raise Exception('')
            except Exception as e:
                seat_category_error = u'Lütfen geçerli kategori no girin.'
            
            try:
                seat_row = request.POST['seat_row']
                if not event.isSeatRowValid(seat_row):
                    raise Exception('')
            except Exception as e:
                seat_row_error = u'Lütfen geçerli bir sıra no girin.'

            try:
                seat_number = request.POST['seat_number']
                intvar = int(seat_number)
            except Exception as e:
                seat_number_error = u'Lütfen geçerli bir koltuk no girin.'
            #TODO:seat_number limit validation

            if ticket_count_error or seat_category_error or seat_row_error or seat_number_error:
                ticket_count_list = valid_ticket_count_range
                seat_category_list = event.getSeatCategories()
                seat_row_list = event.getSeatRows()
                return render(request,'sell/bilet_detaylari.html',
                {'ticket_count_list':ticket_count_list,
                'seat_category_list':seat_category_list,
                'seat_row_list':seat_row_list,
                'ticket_count_error':ticket_count_error,
                'seat_category_error':seat_category_error,
                'seat_row_error':seat_row_error,
                'seat_number_error':seat_number_error})

            request.session['sell_ticket_count'] = ticket_count
            request.session['sell_seat_category'] = seat_category
            request.session['sell_seat_row'] = seat_row
            request.session['sell_seat_number'] = seat_number
            
            return redirect('/fiyatlandir')
        except Exception as e:
            return redirect('/anasayfa')
        
    else:
        if request.GET['event_id']:
            try:
                event_id = request.GET['event_id']
                event = Event.objects.get(id=event_id)
                
                request.session['sell_event_id'] = event_id
                
                ticket_count_list = valid_ticket_count_range
                seat_category_list = event.getSeatCategories()
                seat_row_list = event.getSeatRows()
                
                                
                return render(request,'sell/bilet_detaylari.html',
                {'ticket_count_list':ticket_count_list,
                'seat_category_list':seat_category_list,
                'seat_row_list':seat_row_list})
                
            except Exception as e:
                print '%s (%s)' % (e.message, type(e))
                return redirect('/anasayfa')
        else:
            return redirect('/anasayfa')
            

    
def fiyatlandir(request):
    try:
        event = Event.objects.get(id = request.session['sell_event_id'])
        ticket_count = request.session['sell_ticket_count']
        seat_category = request.session['sell_seat_category']
        seat_row = request.session['sell_seat_row']
        seat_number = request.session['sell_seat_number']
    except Exception as e:
        return redirect('/anasayfa')

    ticket_face_value_error = ''
    ticket_sell_value_error = ''

    if request.method == 'POST':
        try:
            ticket_face_value = request.POST['sell_ticket_face_value']
            ticket_sell_value = request.POST['sell_ticket_sell_value']
            
            try:
                dummy = float(ticket_face_value)
            except Exception as e:
                ticket_face_value_error = u'Lütfen geçerli bir fiyat girin.'

            try:
                dummy = float(ticket_sell_value)
            except Exception as e:
                ticket_sell_value_error = u'Lütfen geçerli bir fiyat girin.'
            
            if (ticket_face_value_error == '') and (ticket_sell_value_error == ''):
                request.session['sell_ticket_face_value'] = ticket_face_value
                request.session['sell_ticket_sell_value'] = ticket_sell_value
            
                return redirect('/teslimat')
                
        except Exception as e:
            return redirect('/anasayfa')
        
    return render(request,'sell/fiyatlandir.html',
    {'event':event,
    'ticket_count':ticket_count,
    'seat_category':seat_category,
    'seat_row':seat_row,
    'seat_number':seat_number,
    'ticket_face_value_error':ticket_face_value_error,
    'ticket_sell_value_error':ticket_sell_value_error})
        
        
    
def teslimat(request):
    ship_name_error = ''
    ship_surname_error = ''
    ship_city_error = ''
    ship_neighbourhood_error = ''
    ship_address_error = ''
    ship_address2_error = ''

    if request.method == 'POST':
        try:
            ship_name = request.POST['ship_name']
            ship_surname = request.POST['ship_surname']
            ship_city = request.POST['ship_city']
            ship_neighbourhood = request.POST['ship_neighbourhood']
            ship_address = request.POST['ship_address']
            ship_address2 = request.POST['ship_address2']
            
            error_message = u'Lütfen geçerli bir değer giriniz.'
            if not re.match(u"^[A-Za-z\sÇçŞşÜüÖöIıİiĞğ]+$", ship_name,re.UNICODE):
                ship_name_error = error_message
            if not re.match(u"^[A-Za-z\sÇçŞşÜüÖöIıİiĞğ]+$", ship_surname,re.UNICODE):
                ship_surname_error = error_message
            if not re.match(u"^[A-Za-z\sÇçŞşÜüÖöIıİiĞğ]+$", ship_city,re.UNICODE):
                ship_city_error = error_message
            if not re.match(u"^[A-Za-z\sÇçŞşÜüÖöIıİiĞğ]+$", ship_neighbourhood,re.UNICODE):
                ship_neighbourhood_error = error_message
            if not re.match("^[0-9A-Za-z:,-./\sÇçŞşÜüÖöIıİiĞğ]+$",ship_address,re.UNICODE):
                ship_address_error = error_message
            if ship_address2 != '' and (not re.match("^[0-9A-Za-z:,-./\sÇçŞşÜüÖöIıİiĞğ]+$",ship_address2,re.UNICODE)):
                ship_address2_error = error_message
            
            if ship_name_error == '' and ship_surname_error == '' and ship_city_error == '' and ship_neighbourhood_error == '' and ship_address_error == '' and ship_address2_error == '':
                request.session['ship_name'] = ship_name
                request.session['ship_surname'] = ship_surname
                request.session['ship_city'] = ship_city
                request.session['ship_neighbourhood'] = ship_neighbourhood
                request.session['ship_address'] = ship_address
                request.session['ship_address2'] = ship_address2
                
                return redirect('/onayla')
            
        except Exception as e:
            # print '%s (%s)' % (e.message, type(e))
            return redirect('/anasayfa')

        
    return render(request,'sell/teslimat.html',{
        'ship_name_error':ship_name_error,
        'ship_surname_error':ship_surname_error,
        'ship_city_error':ship_city_error,
        'ship_neighbourhood_error':ship_neighbourhood_error,
        'ship_address_error':ship_address_error,
        'ship_address2_error':ship_address2_error
    })

def onayla(request):
    try:
        event = Event.objects.get(id=request.session['sell_event_id'])
        ticket_count = request.session['sell_ticket_count']
        seat_category = request.session['sell_seat_category']
        seat_row = request.session['sell_seat_row']
        seat_number = request.session['sell_seat_number']
        ticket_sell_value = request.session['sell_ticket_sell_value']
    except Exception as e:
        # print '%s (%s)' % (e.message, type(e))
        return redirect('/anasayfa')
    
    if request.method == 'POST':
        pass
    return render(request,'sell/onayla.html',{
        'event':event,
        'ticket_count':ticket_count,
        'seat_category':seat_category,
        'seat_row':seat_row,
        'seat_number':seat_number,
        'ticket_sell_value':ticket_sell_value
    })
