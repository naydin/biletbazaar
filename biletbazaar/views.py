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
    
    if request.method == 'POST':
        if 'eventGroupModelForm' in request.POST:
            form = EventGroupModelForm(request.POST)
        if 'eventModelForm' in request.POST:
            form = EventModelForm(request.POST)
        if 'ticketModelForm' in request.POST:
            form = TicketModelForm(request.POST)
        if 'userModelForm' in request.POST:
            form = userModelForm(request.POST)
        if 'landingUserModelForm' in request.POST:
            form = LandingUserModelForm(request.POST)
            
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

    return render(request, 'admin_panel.html', {'eventGroupModelForm': eventGroupModelForm,'eventModelForm':eventModelForm,'ticketModelForm':ticketModelForm,'userModelForm':userModelForm,'landingUserModelForm':landingUserModelForm})

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


def anasayfa(request):
    return render(request,'abc.html',{'base':'/static/'})


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

