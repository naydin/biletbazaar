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

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def hello(request):
    return HttpResponse("Hola world")

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
        
        subject, from_email, to_mail = 'Bilet Bosta Hosgeldiniz Mesaji', 'biletbosta@naydin.webfactional.com', [reqEmail]
        text_content = 'Turkiye 2.el bilet pazari cok yakinda www.biletbosta.com adresinde sizlerle bulusacak!'
 
        message = EmailMessage(subject, text_content, from_email,to_mail)
        message.send()
        
    return render(request,'landing_page.html',{'base':'/static/','error':clientError})

def mail_template(request):
    return render(request,'mail_template.html',{'base':'/static/'})

def send_mail(request):
    subject, from_email, to_mail = 'Bilet Bosta\'ya Hosgeldiniz', 'biletbosta@naydin.webfactional.com','aydinnecati@gmail.com'
    # text_content = 'Turkiye 2.el bilet pazari cok yakinda www.biletbosta.com adresinde sizlerle bulusacak!'
    text_content = 'content'
    html_message = loader.get_template('mail_template.html')
    # message = EmailMessage(subject,text_content,from_email,to_mail,html_message)
    # message.send()
    send_mail(subject, html_message.render(), from_email, [to_mail], fail_silently=False)
    share
    return HttpResponse('oldu')
# def events(request):
#     event_list = getAllEvents()
#     t = get_template('events.html')
#     html = t.render(Context({'event_list':event_list}))
#     # insertEvent("konser",'cok hos')
#     # insertEventt()
# 
#     return HttpResponse(html)

