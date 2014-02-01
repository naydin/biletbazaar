from django.db import models

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

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.EmailField()
    gsm = models.CharField(max_length =20, null=True)
    address = models.CharField(max_length=100, null=True)
    iban = models.CharField(max_length = 25, null=True)
    saleCount = models.IntegerField()
    purchaseCount = models.IntegerField()
    #TODO: Password, name surname

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
    

    # name = models.CharField(max_length = 30)
#     description = models.CharField(max_length = 200)
    
    # def __unicode__(self):
#             return self.name


