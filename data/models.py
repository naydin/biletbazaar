from django.db import models

class EventGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 200)
    category = models.CharField(max_length = 30,null=True)
    saleCount = models.IntegerField()
    photoUrl = models.URLField(null=True)
    #time interval?
    
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    eventGroup = models.ForeignKey(EventGroup)
    place = models.CharField(max_length = 30)
    date = models.DateField()
    city = models.CharField(max_length = 15)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.EmailField()
    gsm = models.CharField(max_length =20, null=True)
    address = models.CharField(max_length=100, null=True)
    iban = models.CharField(max_length = 25, null=True)
    saleCount = models.IntegerField()
    purchaseCount = models.IntegerField()

seatCategorySeparator = '=='
    
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    price = models.DecimalField(max_digits = 8, decimal_places = 2)
    creationDate = models.DateField()
    ticketCount = models.IntegerField()
    seatCategory = models.CharField(max_length = 30)
    
    
    
    # name = models.CharField(max_length = 30)
#     description = models.CharField(max_length = 200)
    
    # def __unicode__(self):
#             return self.name

