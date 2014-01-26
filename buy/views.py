# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context,loader
from data.models import *
from django.shortcuts import render,redirect

import datetime
import re

def biletal1(request):
    if request.method == 'POST':
        try:
            ticket_id = request.session['buy_ticket_id']
            ticket = Ticket.objects.get(id = ticket_id)
            if ticket_count > ticket.ticket_count:
                return redirect('/anasayfa')
            
            ticket_count = request.POST['buy_ticket_count']
            request.session['buy_ticket_count'] = ticket_count
            
            return redirect('/biletal2')
            
        except Exception as e:
            return redirect('/anasayfa')
            

    else:
        try:
            ticket_id = request.GET['ticket_id']
            ticket = Ticket.objects.get(id = ticket_id)
            ticket_count_list = range(1,ticket.ticketCount+1)
            
            request.session['buy_ticket_id'] = ticket_id
            
            return render(request,'buy/biletal1.html',{
                'ticket':ticket,
                'ticket_count_list':ticket_count_list
            })

        except Exception as e:
            # print '%s (%s)' % (e.message, type(e))
            return redirect('/anasayfa')    
    
    
def biletal2(request):
    return render(request,'buy/biletal2.html')
    
def biletal3(request):
    return render(request,'buy/biletal3.html')
    
def biletal4(request):
    return render(request,'buy/biletal4.html')