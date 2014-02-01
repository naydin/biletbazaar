from django import forms
from data.models import *

# class EventGroupForm(forms.Form):    
#     # id = models.AutoField(primary_key=True)
#     name = forms.CharField(max_length = 30)
#     description = forms.CharField(max_length = 200)
#     category = forms.CharField(max_length = 30,required=False)
#     saleCount = forms.IntegerField(required=False)
#     photoUrl = forms.URLField(required=False)



class EventForm(forms.Form):
    # id = models.AutoField(primary_key=True)
    # eventGroup = forms.ForeignKey(EventGroup)
    eventGroup = forms.IntegerField()
    place = forms.CharField(max_length = 30)
    date = forms.DateField()
    city = forms.CharField(max_length = 15)

class UserForm(forms.Form):
    # id = models.AutoField(primary_key=True)
    username = forms.EmailField()
    gsm = forms.CharField(max_length =20, required=False)
    address = forms.CharField(max_length=100, required=False)
    iban = forms.CharField(max_length = 25, required=False)
    saleCount = forms.IntegerField()
    purchaseCount = forms.IntegerField()

class TicketForm(forms.Form):
    # id = models.AutoField(primary_key=True)
    # user = forms.ForeignKey(User)
    user = forms.IntegerField()
    # event = forms.ForeignKey(Event)
    event = forms.IntegerField()
    price = forms.DecimalField(max_digits = 8, decimal_places = 2)
    creationDate = forms.DateField()
    ticketCount = forms.IntegerField()
    seatCategory = forms.CharField(max_length = 30)
    
class LandingUserForm(forms.Form):
    email = forms.EmailField()
    
class ImageDocumentForm(forms.Form):
    docfile = forms.FileField()
    
