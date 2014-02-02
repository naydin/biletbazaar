# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context,loader
from data.models import *
from django.shortcuts import render,redirect

from biletbazaar.validation_util import *

import datetime


def biletal1(request):
    if request.method == 'POST':
        try:
            ticket_id = request.session['buy_ticket_id']
            ticket = Ticket.objects.get(id = ticket_id)            
            ticket_count = request.POST['buy_ticket_count']
            
            if int(ticket_count) > ticket.ticketCount:
                return redirect('/anasayfa')
            
            request.session['buy_ticket_count'] = ticket_count
            
            return redirect('/biletal2')
            
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return redirect('/anasayfa')
            

    else:
        try:
            ticket_id = request.GET['ticket_id']
            ticket = Ticket.objects.get(id = ticket_id)
            ticket_count_list = range(1,ticket.ticketCount+1)
            
            event_id = ticket.event.id
            event = Event.objects.get(id=event_id)
            event_group_idd = event.eventGroup.id
            event_group_photoUrl = EventGroup.objects.get(id=event_group_idd).photoUrl
            print event_group_photoUrl
            
            request.session['buy_ticket_id'] = ticket_id
            
            return render(request,'buy/biletal1.html',{
                'ticket':ticket,
                'ticket_count_list':ticket_count_list,
                'event_group_photoUrl': event_group_photoUrl
            })

        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return redirect('/anasayfa')    
    
    
def biletal2(request):
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
            if ship_address2 != '' and (not validation_util.is_address(ship_address2)):
                ship_address2_error = error_message
            
            if ship_name_error == '' and ship_surname_error == '' and ship_city_error == '' and ship_neighbourhood_error == '' and ship_address_error == '' and ship_address2_error == '':
                request.session['ship_name'] = ship_name
                request.session['ship_surname'] = ship_surname
                request.session['ship_city'] = ship_city
                request.session['ship_neighbourhood'] = ship_neighbourhood
                request.session['ship_address'] = ship_address
                request.session['ship_address2'] = ship_address2
                
                return redirect('/biletal3')
            
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return redirect('/anasayfa')

        
    return render(request,'buy/biletal2.html',{
        'ship_name_error':ship_name_error,
        'ship_surname_error':ship_surname_error,
        'ship_city_error':ship_city_error,
        'ship_neighbourhood_error':ship_neighbourhood_error,
        'ship_address_error':ship_address_error,
        'ship_address2_error':ship_address2_error
    })
    
def biletal3(request):
    card_type_error = ''
    name_error = ''
    surname_error = ''
    card_number_error = ''
    card_expiration_month_error = ''
    card_expiration_year_error = ''
    card_cvc2_error = ''
        
    month_list = []
    for month_number in range(1,13):
        month_list.append('%02d' % month_number)
        
    year_list = []
    for year_number in range(14,26):
        year_list.append('%02d' % year_number)
    
    card_type_list = CreditCardType.objects.all()
    
    if request.method == 'POST':
        try:
            card_type = request.POST['buy_card_type']
            name = request.POST['buy_name']
            surname = request.POST['buy_surname']
            card_number = request.POST['buy_card_number']

            error_message = u'Lütfen geçerli bir değer giriniz.'
            try:
                card_expiration_month = request.POST['buy_card_expiration_month']
            except Exception as e:
                card_expiration_month_error = error_message
                card_expiration_month = ''
            try:
                card_expiration_year = request.POST['buy_card_expiration_year']
            except Exception as e:
                card_expiration_year_error = error_message
                card_expiration_year = ''
            card_cvc2 = request.POST['buy_card_cvc2']
            

            #TODO card_type validation
            if not validation_util.is_all_char_with_whitespace(name):
                name_error = error_message
            if not validation_util.is_all_char(surname):
                surname_error = error_message
            if not (validation_util.is_all_digit(card_number) and len(card_number) == 16):
                card_number_error = error_message
            if not (validation_util.is_all_digit(card_expiration_month) and len(card_expiration_month) == 2):
                card_expiration_month_error = error_message
            if not (validation_util.is_all_digit(card_expiration_year) and len(card_expiration_year) == 2):
                card_expiration_year_error = error_message
            if not (validation_util.is_all_digit(card_cvc2) and len(card_cvc2) == 3):
                card_cvc2_error = error_message
                
            if card_type_error == '' and name_error == '' and surname_error == '' and card_number_error == '' and card_expiration_month_error == '' and card_expiration_year_error == '' and card_cvc2_error =='':
                request.session['buy_name'] = name
                request.session['buy_surname'] = surname
                request.session['buy_card_number'] = card_number
                request.session['buy_card_expiration_month'] = card_expiration_month
                request.session['buy_card_expiration_year'] = card_expiration_year
                request.session['buy_card_cvc2'] = card_cvc2
                
                return redirect('/biletal4')
            
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return redirect('/anasayfa')
    
    return render(request,'buy/biletal3.html',{
        'card_type_list':card_type_list,
        'month_list':month_list,
        'year_list':year_list,
        'card_type_error':card_type_error,
        'name_error':name_error,
        'surname_error':surname_error,
        'card_number_error':card_number_error,
        'card_expiration_month_error':card_expiration_month_error,
        'card_expiration_year_error':card_expiration_year_error,
        'card_cvc2_error':card_cvc2_error
    })
    
def biletal4(request):
    try:
        ticket_id = request.session['buy_ticket_id']
        ticket_count = request.session['buy_ticket_count']
        ticket = Ticket.objects.get(id=ticket_id)
    except Exception as e:
        return redirect('/anasayfa')
        
    return render(request,'buy/biletal4.html',{
        'ticket':ticket,
        'ticket_count':ticket_count
    })


