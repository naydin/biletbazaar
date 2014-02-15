from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

from django.db.models import Avg, Max, Min
from decimal import Decimal


arrayElementSeparator = ',,'

class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15,null=False)

    def __unicode__(self):
        return self.name
        
class EventGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 200)
    category = models.CharField(max_length = 30,null=True)
    saleCount = models.IntegerField(default=0)
    photoUrl = models.URLField(null=True)
    
    def __unicode__(self):
        return self.name
    #time interval?
    
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    eventGroup = models.ForeignKey(EventGroup)
    place = models.CharField(max_length = 30)
    date = models.DateField()
    city = models.ForeignKey(City)
    
    availableCategories = models.CharField(max_length = 100, null=True)
    availableSeatRows = models.CharField(max_length = 50, null=True)
    
    def __unicode__(self):
        return self.eventGroup.name + " "+ self.city.name+ " " + self.place
        
    def addSeatCategory(self,seatCategory):
        if self.availableCategories:
            self.availableCategories += arrayElementSeparator + seatCategory
        else:
            self.availableCategories = seatCategory
            
    def getSeatCategories(self):
        if self.availableCategories:
            return self.availableCategories.split(arrayElementSeparator)
        else:
            return None
    
    def isSeatCategoryValid(self, seatCategory):
        seatCategories = self.getSeatCategories()
        for category in seatCategories:
            if seatCategory == category:
                return True
        
        return False
         
    def addSeatRow(self,seatRow):
        if self.availableSeatRows:
            self.availableSeatRows += arrayElementSeparator + seatRow
        else:
            self.availableSeatRows = seatRow
            
    def getSeatRows(self):
        if self.availableSeatRows:
            return self.availableSeatRows.split(arrayElementSeparator)
        else:
            return None
            
    def isSeatRowValid(self, seatRow):
        seatRows = self.getSeatRows()
        for row in seatRows:
            if seatRow == row:
                return True
        
        return False
    
    
    
    
    
    def calculateTickets(self):
        return Ticket.objects.filter(event = self.id).count()

    total_tickets = property(calculateTickets)
    
    
    def minTicket(self):
        t = Ticket.objects.filter(event = self.id).aggregate(Min('price'))
        if(t["price__min"]==None):
            return '-'
        else:
            return t["price__min"]

    min_ticket = property(minTicket)
    
    
   

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=self.normalize_email(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user    

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.EmailField(unique=True,max_length=50)
    gsm = models.CharField(max_length =20, null=True)
    address = models.CharField(max_length=100, null=True)
    iban = models.CharField(max_length = 25, null=True)
    saleCount = models.IntegerField(null=True)
    purchaseCount = models.IntegerField(null=True)
    first_name = models.CharField(null=True, max_length=20)
    last_name = models.CharField(null=True,max_length=15)
    # password_token = models.CharField(null = True, max_length = 50)
    #password comes from base user

    USERNAME_FIELD = 'username'

    objects = UserManager()
    
    def __unicode__(self):
        return self.username
    
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    price = models.DecimalField(max_digits = 8, decimal_places = 2)
    faceValue = models.DecimalField(max_digits = 8, decimal_places = 2)
    creationDate = models.DateField()
    ticketCount = models.IntegerField()
    
    seatCategory = models.CharField(max_length = 20, null=True)
    seatRow = models.CharField(max_length = 20, null=True)
    seatNumber = models.CharField(max_length=20, null=True)
    
#     seatNumberFrom = models.CharField(max_length=20, null=True)
#     seatNumberTo = models.CharField(max_length=20, null=True)
#     
#     isActive = models.BooleanField(null=False,default=True)
# 
# class SaleStatus(object):#enum
#     waitingSellerApproval = 1
#     sellerApproved = 2
#     shipping = 3
#     buyerApproved = 4
# 
# class Sale(models.Model):
#     id = models.AutoField(primary_key=True)
#     ticket = models.ForeignKey(Ticket)
#     buyer = models.ForeignKey(User)
#     seatNumberFrom = models.CharField(null=True,max_length=20)
#     seatNumberTo = models.CharField(null=True,max_length=20)
#     saleStatus = models.IntegerField(null=False,default=SaleStatus.waitingSellerApproval)
# 
#     def getSeller(self):
#         return ticket.user
#     seller = property(getSeller)
#     #TODO: dates for sale statuses should be added?
    
class ShipmentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 20)
    surname = models.CharField(max_length = 15)
    city = models.CharField(max_length = 20)
    neighbourhood = models.CharField(max_length = 20) #semt
    address = models.CharField(max_length = 50)
    address2 = models.CharField(max_length = 50)
    ticket = models.OneToOneField(Ticket)

class PaymentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 20)
    surname = models.CharField(max_length = 15)
    iban = models.CharField(max_length = 16, null=True)
    ticket = models.OneToOneField(Ticket)

class CreditCardType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 20)
    
class LandingUser(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    
class ImageDocument(models.Model):
    docfile = models.FileField(upload_to='event_group_photos')
    
class BizeUlasin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.CharField(max_length=200)
    

class EtkinlikBildir(models.Model):
    id = models.AutoField(primary_key=True)
    isim = models.CharField(max_length=30)
    mekan = models.CharField(max_length=30)
    zaman = models.CharField(max_length=30)
    sehir = models.CharField(max_length=30)
    link = models.CharField(max_length=30)
    email = models.EmailField()
    
    

    # name = models.CharField(max_length = 30)
#     description = models.CharField(max_length = 200)
    
    # def __unicode__(self):
#             return self.name


