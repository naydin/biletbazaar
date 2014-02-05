# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext
from django.template import loader
from data.models import *
from django.shortcuts import render,redirect

from biletbazaar.validation_util import *

import datetime


def biletal1(request):
    if request.method == 'POST':
        if 'devam' in request.POST:
            
            try:
                ticket_id = request.session['buy_ticket_id']
                ticket = Ticket.objects.get(id = ticket_id)
                
                ticket_count = request.POST['buy_ticket_count']
               
                request.session['buy_ticket_count'] = ticket_count
                
                return redirect('/biletal2')
                
            except Exception as e:
                return redirect('/anasayfa')
        else:
            try:
                ticket_count = request.POST['buy_ticket_count']
                request.session['buy_ticket_count'] = ticket_count
                
                ticket_id = request.GET['ticket_id']
                ticket = Ticket.objects.get(id = ticket_id)
                ticket_count_list = range(1,ticket.ticketCount+1)
                
                event=Event.objects.get(id = ticket.event.id)
                event_group_id = event.eventGroup.id
                event_group_photoUrl = EventGroup.objects.get(id = event_group_id).photoUrl
                
               
                print ticket_count
                return render(request,'buy/biletal1.html',{
                    'ticket':ticket,
                    'ticket_count_list':ticket_count_list,
                    'ticket_count':int(ticket_count),
                    'event_group_photoUrl':event_group_photoUrl
                })

            except Exception as e:
                # print '%s (%s)' % (e.message, type(e))
                return redirect('/anasayfa')
            
            

    else:
        try:
            ticket_id = request.GET['ticket_id']
            ticket = Ticket.objects.get(id = ticket_id)
            ticket_count_list = range(1,int(ticket.ticketCount)+1)
            
            request.session['buy_ticket_id'] = ticket_id
            
            event=Event.objects.get(id = ticket.event.id)
            event_group_id = event.eventGroup.id
            event_group_photoUrl = EventGroup.objects.get(id = event_group_id).photoUrl
          
            
            return render(request,'buy/biletal1.html',{
                'ticket':ticket,
                'ticket_count_list':ticket_count_list,
                'ticket_count':1,
                'event_group_photoUrl':event_group_photoUrl
            })

        except Exception as e:
            # print '%s (%s)' % (e.message, type(e))
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
    
    card_type_list = CreditCardType.objects.all()
    return render(request,'buy/biletal3.html',{
        'card_type_list':card_type_list
    })
    
def biletal4(request):
    return render(request,'buy/biletal4.html')