# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import RequestContext
from django.template import loader
from data.eventManager import *
from data.models import *
from django.shortcuts import render,redirect,render_to_response
from forms import *
from modelForms import *
from django.db.models import Max
from static_data import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout,REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url

import datetime
import re

selected_city_name_field = "selected_city_name"

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        if 'login_form' in request.POST:
            print '==' + REDIRECT_FIELD_NAME
            redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                               request.GET.get(REDIRECT_FIELD_NAME, ''))
            print '**' + redirect_to
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
                            
            username = request.POST['username']
            password = request.POST['password']
            print username + '==' + password
            user = authenticate(username=username, password=password)
            print user
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(redirect_to)
        else:#TODO: signup should be implemented
            pass
    return render_to_response('login.html', context_instance=RequestContext(request))

#reset all data in bilet bosta database
def reset_data(request):
    try:
        reset_static_data()
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))

    return HttpResponse("Reset Successful.")


#admin panel: data entry into Bilet Bosta Database
@login_required(login_url='/login')
def admin_panel(request):
    eventGroupModelForm = EventGroupModelForm()
    eventModelForm = EventModelForm()
    ticketModelForm = TicketModelForm()
    userModelForm = UserModelForm()
    landingUserModelForm = LandingUserModelForm()
    cityModelForm = CityModelForm()
    imageDocumentForm = ImageDocumentForm()
    
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
        if 'imageDocumentForm' in request.POST:
            form = ImageDocumentForm(request.POST,request.FILES)
            
        if form.is_valid():
            if 'imageDocumentForm' in request.POST:
                if form.is_valid():
                    newDoc = ImageDocument(docfile = request.FILES['docfile'])
                    newDoc.save()
                    
            else:
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
            if 'imageDocumentForm' in request.POST:
                imageDocumentForm = form
                
    return render(request, 'admin_panel.html', {
        'eventGroupModelForm': eventGroupModelForm,
        'eventModelForm':eventModelForm,
        'ticketModelForm':ticketModelForm,
        'userModelForm':userModelForm,
        'landingUserModelForm':landingUserModelForm,
        'cityModelForm':cityModelForm,
        'imageDocumentForm':imageDocumentForm
    })
    

#landing page
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
    


#anasayfa --> view ismi anasayfa, template ismi main_page..ikisinden biri seçilip aynı olması sağlanmalı
def anasayfa(request):
    # max_sale_count = EventGroup.objects.all().aggregate(Max('saleCount'))['saleCount__max']
    # event_group_list = EventGroup.objects.filter(saleCount = max_sale_count)
    # event_group = event_group_list[0]
    # event_list = event_group.event_set.all()
	
	request.session[selected_city_name_field] = u"Tüm Türkiye"
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


#send email content 
def send_maill(email):
    subject, from_email, to = 'Bilet Bosta\'ya Hosgeldiniz', 'info@biletbosta.com',email
    text_content = ''
    c = RequestContext(request,{'ig_url':'http://www.biletbosta.com/static/bilet-bosta-reklam.png'})
    t = loader.get_template('mail_template.html')
    html_content = t.render(c)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

 
def event_group(request):

	 
	if request.method == 'GET':
		try:
    	
			if(request.session[selected_city_name_field]==u"Tüm Türkiye"):
				selected_city_name = ""
			else:
				selected_city_name = request.session[selected_city_name_field]
            	
            	
            	
			event_group_id = request.GET['event_group_id']
			eventgroup = EventGroup.objects.get(id=event_group_id)
			events = Event.objects.filter(eventGroup__id = event_group_id, city__name__icontains=selected_city_name)
        
   
			event_group_name = eventgroup.name
			event_group_description = eventgroup.description
			event_group_category = eventgroup.category
			event_group_saleCount = eventgroup.saleCount
			event_group_photoUrl = eventgroup.photoUrl
			city_list = City.objects.all()
			
			
			
			return render(request,'events/event_group.html',
			{'event_group_name':event_group_name,
			'event_group_description':event_group_description,
			'event_group_category':event_group_category,
			'event_group_saleCount':event_group_saleCount,
			'event_group_photoUrl':event_group_photoUrl,
			'events' : events,
			'city_list' : city_list,
			'selected_city_name' : selected_city_name, 
			'city_name_all_cities':u"Tüm Türkiye"
			
			})

		except Exception as e:
			print '%s (%s)' % (e.message, type(e))
			return redirect('/anasayfa')
	elif request.method == 'POST':
        	selected_city_name = u''
        	#if a city is posted take that as selected city
    		try:
    			if(request.POST['city_select']==u"Tüm Türkiye"):
    				selected_city_name = ""
    			else:
        			selected_city_name = request.POST['city_select']
    		except Exception as e:
        		# print '%s (%s)' % (e.message, type(e))
        		pass
        	
        	
        	event_group_id = request.GET['event_group_id']
                eventgroup = EventGroup.objects.get(id=event_group_id)
                events = Event.objects.filter(eventGroup__id = event_group_id, city__name__icontains=selected_city_name)
                
           
                event_group_name = eventgroup.name
                event_group_description = eventgroup.description
                event_group_category = eventgroup.category
                event_group_saleCount = eventgroup.saleCount
                event_group_photoUrl = eventgroup.photoUrl
                city_list = City.objects.all()
                
                
                
                return render(request,'events/event_group.html',
                {'event_group_name':event_group_name,
                'event_group_description':event_group_description,
                'event_group_category':event_group_category,
                'event_group_saleCount':event_group_saleCount,
              	'event_group_photoUrl':event_group_photoUrl,
              	'events' : events,
              	'city_list' : city_list,
              	'selected_city_name' : selected_city_name, 
              	'city_name_all_cities':u"Tüm Türkiye"
              	
                })
        		
        	
	else:
            return redirect('/anasayfa')    
            
def event(request):
	event_id = request.GET['event_id']
	if request.method == 'GET':
		tickets = Ticket.objects.filter(event__id = event_id).order_by('price')
		selected_category=u"Tümü"
		sort_type=u"bilet fiyatı"
	elif request.method == 'POST':
		selected_category = u''
		if request.POST['category_select'] == u"Tümü":
			selected_category = ""
		else:
			selected_category = request.POST['category_select']

		sort_type = request.POST['sirala']
    
		if sort_type == u"bilet fiyatı":
			tickets = Ticket.objects.filter(event__id = event_id,seatCategory__icontains=selected_category).order_by('price')
		else:
			tickets = Ticket.objects.filter(event__id = event_id,seatCategory__icontains=selected_category).order_by('ticketCount')
	else:
		pass          
        
        
	try:  
		event = Event.objects.get(id=event_id)       
		event_group_idd = event.eventGroup.id       
		event_group_name = EventGroup.objects.get(id=event_group_idd).name
		event_group_photoUrl = EventGroup.objects.get(id=event_group_idd).photoUrl
		print event_group_photoUrl
		        
		events = Event.objects.filter(eventGroup__id = event_group_idd)
        
	            
	            
		event_place = event.place
		event_date = event.date
		event_city = event.city
		
		event_categories = event.getSeatCategories()
	            
		return render(request,'events/event.html',
	            {'event_place':event_place,
	            'event_date':event_date,
	            'event_city':event_city,
	            'event_group_name':event_group_name,
	            'event_group_photoUrl' : event_group_photoUrl,
	          	'tickets' : tickets,
	          	'events' : events,
	          	'event_categories' : event_categories,
	          	'all_categories':u"Tümü",
	          	'selected_category':selected_category,
	          	'sort_type':sort_type
	    
	          	
	            })
	                
        	
	except Exception as e:
		print '%s (%s)' % (e.message, type(e))
		return redirect('/anasayfa')
	   	
   
def hesabim(request):
	return render(request,'hesabim.html')
       
def bize_ulasin(request):
	if request.method == 'GET':
		return render(request,'bize_ulasin.html')
	elif request.method == 'POST':
		
		bize_ulasin = BizeUlasin()
		
		bize_ulasin.name = request.POST['name']
		bize_ulasin.email = request.POST['email']
		bize_ulasin.message = request.POST['message']
        
		bize_ulasin.save()
		
		return redirect('/anasayfa')
	else:	
		return redirect('/hesabim')
		

def search_result(request):
	if request.method == 'POST':
		if request.POST['search_here']:
			query = request.POST['search_here']
			event_list = Event.objects.filter(eventGroup__name__icontains=query)
		return render(request,'search_results.html',{'event_list':event_list})
	else:
		return redirect('/search_result')
	
		
	