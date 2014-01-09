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

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def hello(request):
    return HttpResponse("Hola world")

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
        
        # subject, from_email, to_mail = 'Bilet Bosta Hosgeldiniz Mesaji', 'biletbosta@naydin.webfactional.com', [reqEmail]
#         text_content = 'Turkiye 2.el bilet pazari cok yakinda www.biletbosta.com adresinde sizlerle bulusacak!'
#  
#         message = EmailMessage(subject, text_content, from_email,to_mail)
#         message.send()
        send_maill(reqEmail)
        
    return render(request,'landing_page.html',{'base':'/static/','error':clientError})

def mail_template(request):
    return render(request,'mail_template.html',{'base':'/static/'})


selected_city_id_field = "selected_city_id"

def anasayfa(request):
    # max_sale_count = EventGroup.objects.all().aggregate(Max('saleCount'))['saleCount__max']
    # event_group_list = EventGroup.objects.filter(saleCount = max_sale_count)
    # event_group = event_group_list[0]
    # event_list = event_group.event_set.all()
    
    selected_city_id = ""
    selected_city_name = ""
    
    if selected_city_id_field in request.COOKIES:
        request.session[selected_city_id_field] = request.COOKIES[selected_city_id_field]
        city = City.objects.get(id=request.COOKIES[selected_city_id_field])
        selected_city_name = city.name
        print "oldu" + request.COOKIES[selected_city_id_field]
    
    try:
        selected_city_name = request.POST['city_select']
        city = City.objects.get(name=selected_city_name)
        request.session[selected_city_id_field] = city.id
        selected_city_id = city.id
    except Exception as e:
        # print '%s (%s)' % (e.message, type(e))
        selected_city_id = ""
    
    event_group_list = EventGroup.objects.all().order_by('-saleCount')[0:5]

    # if len(event_group_list) > 5:
    #     event_group_list = event_group_list[0:5]
    
    # event_list = []
    # for event_group in event_group_list:
    #     event_list_temp = event_group.event_set.filter(city='istanbul')
    #     if len(event_list_temp) >= 1:
    #         event_list.append(event_list_temp[0])

    event_list = Event.objects.filter(city__name='Istanbul').order_by('date')[0:10]
    
    ticket_list = Ticket.objects.filter(event__city__name='Istanbul').order_by('price')[0:5]
    
    city_list = City.objects.all()
    
    response = render(request,'main_page.html',{'base':'/static/','event_list':event_list,'event_group_list':event_group_list,
    'ticket_list':ticket_list,"city_list":city_list,'selected_city_name':selected_city_name})

    if selected_city_id != "":
        response.set_cookie(selected_city_id_field,selected_city_id)
        
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

# def events(request):
#     event_list = getAllEvents()
#     t = get_template('events.html')
#     html = t.render(Context({'event_list':event_list}))
#     # insertEvent("konser",'cok hos')
#     # insertEventt()
# 
#     return HttpResponse(html)

