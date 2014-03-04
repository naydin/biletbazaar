# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from data.models import *
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

import datetime
from biletbazaar.validation_util import *
from biletbazaar.session_util import *

def base(request):
    selected_city_name = u''
    try:
        selected_city_name = request.session[kselected_city]
    except Exception as e:
        selected_city_name = u''
        
    if request.method == 'POST':
        if request.POST['search_here']:
            search_event_group_name = request.POST['search_here']
            event_group = EventGroup.objects.filter(name__icontains=search_event_group_name)
            
    event_group_list = EventGroup.objects.all()
    
    return render(request,'sell/bilet_ilan.html',{'base':'/static/','event_group_list':event_group_list,'event_list':event_list})

# sell step 1 : etkinlik search
def bilet_ilan(request):
    selected_city_name = u''
    try:
        selected_city_name = request.session[kselected_city]
    except Exception as e:
        selected_city_name = u''
    
    event_list = []
    if request.method == 'POST':
        if 'search_event_group_name' in request.POST:
            search_event_group_name = request.POST['search_event_group_name']
            event_list = Event.objects.filter(eventGroup__name__icontains=search_event_group_name,city__name__icontains=selected_city_name)
        elif 'gonder' in request.POST:
            isim = request.POST['isim']
            mekan = request.POST['mekan']
            zaman = request.POST['zaman']
            sehir = request.POST['sehir']
            link = request.POST['link']
            email = request.POST['email']
            
            etkinlik_bildir = EtkinlikBildir()
            etkinlik_bildir.isim = isim
            etkinlik_bildir.mekan = mekan
            etkinlik_bildir.zaman = zaman
            etkinlik_bildir.sehir = sehir
            etkinlik_bildir.link = link
            etkinlik_bildir.email = email
            
            etkinlik_bildir.save()
        else:
            return redirect('/anasayfa')
            
            
               
    event_group_list = EventGroup.objects.all()
    
    return render(request,'sell/bilet_ilan.html',{'base':'/static/','event_group_list':event_group_list,'event_list':event_list})

valid_ticket_count_range = range(1,7)

#sell step2 : bilet detaylari page
def bilet_detaylari(request):
    if request.method == 'POST':
        try:        
            event_id = request.session[ksell_event_id]
            event = Event.objects.get(id=event_id)
            
            ticket_count = ''
            seat_category = ''
            seat_row = ''
            seat_number_from = ''
            seat_number_to = ''
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
            
            if event.getSeatCategories():
                try:
                    seat_category = request.POST['seat_category']
                    if not event.isSeatCategoryValid(seat_category):
                        raise Exception('')
                except Exception as e:
                    seat_category_error = u'Lütfen geçerli kategori no girin.'
            
            if event.getSeatRows():
                try:
                    seat_row = request.POST['seat_row']
                    if not event.isSeatRowValid(seat_row):
                        raise Exception('')
                except Exception as e:
                    seat_row_error = u'Lütfen geçerli bir sıra no girin.'

                try:
                    seat_number_from = request.POST['seat_number_from']
                    seat_number_to = request.POST['seat_number_to']
                    intvar1 = int(seat_number_from)
                    intvar2 = int(seat_number_to)
                    if ((intvar2 - intvar1)+1) != int(ticket_count) :
                        raise Exception('')
                except Exception as e:
                    seat_number_error = u'Kontrol ediniz.'
                
           
            #TODO:seat_number limit validation

            if ticket_count_error =='' and seat_category_error == '' and seat_row_error == '' and seat_number_error == '' :
                request.session[ksell_ticket_count] = ticket_count
                request.session[ksell_seat_category] = seat_category
                request.session[ksell_seat_row] = seat_row
                request.session[ksell_seat_number_from] = seat_number_from
                request.session[ksell_seat_number_to] = seat_number_to
            
                return redirect('/fiyatlandir')
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return redirect('/anasayfa')      
                
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
        'seat_number_error':seat_number_error,
      
        })

            
        
        
    else:
        if request.GET['event_id']:
            try:
                event_id = request.GET['event_id']
                event = Event.objects.get(id=event_id)
                
                request.session[ksell_event_id] = event_id
                
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
            

#sell step 3: fiyatlandır page    
def fiyatlandir(request):
    try:
        event = Event.objects.get(id = request.session[ksell_event_id])
        ticket_count = request.session[ksell_ticket_count]
        seat_category = request.session[ksell_seat_category]
        seat_row = request.session[ksell_seat_row]
        seat_number_from = request.session[ksell_seat_number_from]
        seat_number_to = request.session[ksell_seat_number_to]
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
                request.session[ksell_ticket_face_value] = ticket_face_value
                request.session[ksell_ticket_sell_value] = ticket_sell_value
            
                return redirect('/teslimat')
                
        except Exception as e:
            return redirect('/anasayfa')
     
    cheapest_ticket = Ticket.objects.filter(seatCategory=seat_category).order_by('price')[0]
       
    return render(request,'sell/fiyatlandir.html',
    {'event':event,
    'ticket_count':int(ticket_count),
    'seat_category':seat_category,
    'seat_row':seat_row,
    'seat_number_from':seat_number_from,
    'seat_number_to':seat_number_to,
    'cheapest_ticket':cheapest_ticket,
    'ticket_face_value_error':ticket_face_value_error,
    'ticket_sell_value_error':ticket_sell_value_error})
        
        
#sell step 4 : teslimat page    
@login_required(login_url='/login')
def teslimat(request):
    ship_name_error = ''
    ship_surname_error = ''
    ship_city_error = ''
    ship_neighbourhood_error = ''
    ship_address_error = ''
    

    if request.method == 'POST':
        try:
            ship_name = request.POST['ship_name']
            ship_surname = request.POST['ship_surname']
            ship_city = request.POST['ship_city']
            ship_neighbourhood = request.POST['ship_neighbourhood']
            ship_address = request.POST['ship_address']
           
            
            error_message = u'Lütfen geçerli bir değer giriniz.'
            if not validation_util.is_all_char_with_whitespace(ship_name):
                ship_name_error = error_message
            if not validation_util.is_all_char(ship_surname):
                ship_surname_error = error_message
            if not validation_util.is_all_char(ship_city):
                ship_city_error = error_message
            if not validation_util.is_all_char(ship_neighbourhood):
                ship_neighbourhood_error = error_message
            if not validation_util.is_address(ship_address):
                ship_address_error = error_message
            
            
            if ship_name_error == '' and ship_surname_error == '' and ship_city_error == '' and ship_neighbourhood_error == '' and ship_address_error == '' :
                request.session[ksell_ship_name] = ship_name
                request.session[ksell_ship_surname] = ship_surname
                request.session[ksell_ship_city] = ship_city
                request.session[ksell_ship_neighbourhood] = ship_neighbourhood
                request.session[ksell_ship_address] = ship_address
                
                
                return redirect('/onayla')
            
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return redirect('/anasayfa')

        
    return render(request,'sell/teslimat.html',{
        'ship_name_error':ship_name_error,
        'ship_surname_error':ship_surname_error,
        'ship_city_error':ship_city_error,
        'ship_neighbourhood_error':ship_neighbourhood_error,
        'ship_address_error':ship_address_error,
        
    })


#sell step 5: onayla page
@login_required(login_url='/login')
def onayla(request):
    name_error = ''
    surname_error = ''
    iban_error = ''
    
    try:
        event = Event.objects.get(id=request.session[ksell_event_id])
        ticket_count = request.session[ksell_ticket_count]
        seat_category = request.session[ksell_seat_category]
        seat_row = request.session[ksell_seat_row]
        seat_number_from = request.session[ksell_seat_number_from]
        seat_number_to = request.session[ksell_seat_number_to]
        ticket_sell_value = request.session[ksell_ticket_sell_value]
    except Exception as e:
        # print '%s (%s)' % (e.message, type(e))
        return redirect('/anasayfa')
    
    if request.method == 'POST':
        try:
            sell_name = request.POST['sell_name']
            sell_surname = request.POST['sell_surname']
            sell_iban = request.POST['sell_iban']
                        
            error_message = u'Lütfen geçerli bir değer girin.'
            if not validation_util.is_all_char_with_whitespace(sell_name):
                name_error = error_message
            if not validation_util.is_all_char(sell_surname):
                surname_error = error_message
            if not ( (len(sell_iban) == 16) and validation_util.is_all_digit(sell_iban)):
                iban_error = error_message
            
            if name_error == '' and surname_error == '' and iban_error == '':
                event = Event.objects.get(id = request.session[ksell_event_id])
                ticket_count = request.session[ksell_ticket_count]
                seat_category = request.session[ksell_seat_category]
                seat_row = request.session[ksell_seat_row]
                seat_number_from = request.session[ksell_seat_number_from]
                seat_number_to = request.session[ksell_seat_number_to]
                ticket_face_value = request.session[ksell_ticket_face_value]
                ticket_sell_value = request.session[ksell_ticket_sell_value]
                ship_name = request.session[ksell_ship_name]
                ship_surname = request.session[ksell_ship_surname]
                ship_city = request.session[ksell_ship_city]
                ship_neighbourhood = request.session[ksell_ship_neighbourhood]
                ship_address = request.session[ksell_ship_address]
               
                
                shipment_info = ShipmentInfo()
                shipment_info.name = ship_name
                shipment_info.surname = ship_surname
                shipment_info.city = ship_city
                shipment_info.neighbourhood = ship_neighbourhood
                shipment_info.address = ship_address
                
                
                payment_info = PaymentInfo()
                payment_info.name = sell_name
                payment_info.surname = sell_surname
                payment_info.iban = sell_iban
                
                #todo:ticket should be connected with the loggedin user
                user = request.user
                
                ticket = Ticket()
                ticket.user = user
                ticket.event = event
                ticket.price = ticket_sell_value
                ticket.faceValue = ticket_face_value
                ticket.creationDate = datetime.datetime.now()
                ticket.ticketCount = ticket_count
                
                ticket.seatCategory = seat_category
                ticket.seatRow = seat_row
                ticket.seatNumberFrom = seat_number_from
                ticket.seatNumberTo = seat_number_to
                
                ticket.save()
                
                shipment_info.ticket = ticket
                payment_info.ticket = ticket
                
                
                #TODO aşağıdaki save'ler çalışmıyor!
                shipment_info.save()
                payment_info.save()
                
                request.session[ksell_ticket_id] = ticket.id
                
                return redirect('/satis_onay')
            
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return redirect('/anasayfa')
        
        

    return render(request,'sell/onayla.html',{
        'event':event,
        'ticket_count':int(ticket_count),
        'seat_category':seat_category,
        'seat_row':seat_row,
        'seat_number_from':seat_number_from,
        'seat_number_to':seat_number_to,
        'ticket_sell_value':ticket_sell_value,
        'name_error':name_error,
        'surname_error':surname_error,
        'iban_error':iban_error
    })

def satis_onay(request):
    
    ticket = Ticket.objects.get(id = request.session[ksell_ticket_id])
    
    session_util.clear_sell_steps1234(request)
    return render(request,'sell/share_ticket.html',{
        'ticket':ticket,
                                                   
    })