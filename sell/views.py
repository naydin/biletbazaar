# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context,loader
from data.models import *
from django.shortcuts import render,redirect

import datetime
import re


# sell step 1 : etkinlik search
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

#sell step2 : bilet detaylari page
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
            

#sell step 3: fiyatlandır page    
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
        
        
#sell step 4 : teslimat page    
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


#sell step 5: onayla page
def onayla(request):
    name_error = ''
    surname_error = ''
    iban_error = ''
    
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
        try:
            sell_name = request.POST['sell_name']
            sell_surname = request.POST['sell_surname']
            sell_iban = request.POST['sell_iban']
                        
            error_message = u'Lütfen geçerli bir değer girin.'
            if not re.match(u"^[A-Za-z\sÇçŞşÜüÖöIıİiĞğ]+$", sell_name,re.UNICODE):
                name_error = error_message
            if not re.match(u"^[A-Za-zÇçŞşÜüÖöIıİiĞğ]+$", sell_surname,re.UNICODE):
                surname_error = error_message
            if not ((len(sell_iban) == 16) and re.match(u"^[0-9]+$", sell_iban,re.UNICODE) ):
                iban_error = error_message
            
            if name_error == '' and surname_error == '' and iban_error == '':
                event = Event.objects.get(id = request.session['sell_event_id'])
                ticket_count = request.session['sell_ticket_count']
                seat_category = request.session['sell_seat_category']
                seat_row = request.session['sell_seat_row']
                seat_number = request.session['sell_seat_number']
                ticket_face_value = request.session['sell_ticket_face_value']
                ticket_sell_value = request.session['sell_ticket_sell_value']
                ship_name = request.session['ship_name']
                ship_surname = request.session['ship_surname']
                ship_city = request.session['ship_city']
                ship_neighbourhood = request.session['ship_neighbourhood']
                ship_address = request.session['ship_address']
                ship_address2 = request.session['ship_address2']
                
                shipment_info = ShipmentInfo()
                shipment_info.name = ship_name
                shipment_info.surname = ship_surname
                shipment_info.city = ship_city
                shipment_info.neighbourhood = ship_neighbourhood
                shipment_info.address = ship_address
                shipment_info.address2 = ship_address2
                
                payment_info = PaymentInfo()
                payment_info.name = sell_name
                payment_info.surname = sell_surname
                payment_info.iban = sell_iban
                
                #todo:ticket should be connected with the loggedin user
                user = User.objects.all()[0]
                
                ticket = Ticket()
                ticket.user = user
                ticket.event = event
                ticket.price = ticket_sell_value
                ticket.faceValue = ticket_face_value
                ticket.creationDate = datetime.datetime.now()
                ticket.ticketCount = ticket_count
                
                ticket.seatCategory = seat_category
                ticket.seatRow = seat_row
                ticket.seatNumber = seat_number
                
                shipment_info.ticket = ticket
                payment_info.ticket = ticket
                
                ticket.save()
                shipment_info.save()
                payment_info.save()
                
                return redirect('/anasayfa')
            
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return redirect('/anasayfa')
        
        

    return render(request,'sell/onayla.html',{
        'event':event,
        'ticket_count':ticket_count,
        'seat_category':seat_category,
        'seat_row':seat_row,
        'seat_number':seat_number,
        'ticket_sell_value':ticket_sell_value,
        'name_error':name_error,
        'surname_error':surname_error,
        'iban_error':iban_error
    })