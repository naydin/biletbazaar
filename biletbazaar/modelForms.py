from django.forms import ModelForm
from data.models import *
from django.contrib.admin.widgets import AdminDateWidget

class EventGroupModelForm(ModelForm):
    class Meta:
        model = EventGroup
        # fields = ['name','description','category','saleCount','photoUrl']
        
class EventModelForm(ModelForm):
    class Meta:
        model = Event
        
class UserModelForm(ModelForm):
    class Meta:
        model = User
        
class TicketModelForm(ModelForm):
    class Meta:
        model = Ticket
        
class LandingModelForm(ModelForm):
    class Meta:
        model = LandingUser
