# -*- coding: utf-8 -*-

from data.models import *
import datetime
from random import randrange
import string
import random

def reset_static_data():
    users = User.objects.all()
    for user in users:
        user.delete()
    
    tickets = Ticket.objects.all()
    for ticket in tickets:
        ticket.delete()
        
    events = Event.objects.all()
    for event in events:
        event.delete()

    cities = City.objects.all()
    for city in cities:
        city.delete()
    
    event_groups = EventGroup.objects.all()    
    for event_group in event_groups:
        event_group.delete()
    
    
    istanbul = City()
    istanbul.name = "İstanbul"
    istanbul.save()

    ankara = City()
    ankara.name = "Ankara"
    ankara.save()
    
    izmir = City()
    izmir.name = "İzmir"
    izmir.save()
    
    cities = City.objects.all()

    eg1 = EventGroup()
    eg1.name = "Duman"
    eg1.description = "Bir Bostanci Klasiği"
    eg1.category = "Müzik"
    eg1.saleCount = 100
    eg1.photoUrl = "http://www.biletix.com/static/images/live/event/eventimages/Duman_bgm1.jpg"
    eg1.save()
    
    eg2 = EventGroup()
    eg2.name = "Mor ve Ötesi"
    eg2.description = "İyi konser. Kaçırma!"
    eg2.category = "Müzik"
    eg2.saleCount = 10
    eg2.photoUrl = "http://www.biletix.com/static/images/live/event/eventimages/mor_ve_otesi_02.jpg"
    eg2.save()
    
    eg3 = EventGroup()
    eg3.name = "Sezen Aksu"
    eg3.description = "Minik Serçe."
    eg3.category = "Müzik"
    eg3.saleCount = 55
    eg3.photoUrl = "http://www.biletix.com/static/images/live/event/groupimages/sezen_aksu_02.jpg"
    eg3.save()
        
    eg4 = EventGroup()
    eg4.name = "Tarkan"
    eg4.description = "Oynama şıkıdım şıkıdım."
    eg4.category = "Müzik"
    eg4.saleCount = 200
    eg4.photoUrl = "http://www.biletix.com/static/images/live/event/eventimages/tarkan2012.jpg"
    eg4.save()
    
    eg5 = EventGroup()
    eg5.name = "Mehmet Erdem"
    eg5.description = "Burak ın sevdiği var ya ondan."
    eg5.category = "Müzik"
    eg5.saleCount = 5
    eg5.photoUrl = "http://www.biletix.com/static/images/live/event/eventimages/mehmet_erdem.jpg"
    eg5.save()
    
    eg6 = EventGroup()
    eg6.name = "Rihanna"
    eg6.description = "Rihanna Diamonds Dünya Turnesi."
    eg6.category = "Müzik"
    eg6.saleCount = 250
    eg6.photoUrl = "http://www.biletix.com/static/images/live/event/eventimages/rihanna.jpg"
    eg6.save()
    
    eg7 = EventGroup()
    eg7.name = "Levent Yuksel"
    eg7.description = "Askerden sonra ilk konseri. Kaçırma!"
    eg7.category = "Müzik"
    eg7.saleCount = 60
    eg7.photoUrl = "http://www.biletix.com/static/images/live/event/eventimages/levent_yuksel_jollyjoker.jpg"
    eg7.save()
    
    eg8 = EventGroup()
    eg8.name = "Teoman"
    eg8.description = "Sağdan soldan arakladığı bikaç akor melankoli falan felan işte anladın sen onu."
    eg8.category = "Müzik"
    eg8.saleCount = 80
    eg8.photoUrl = "http://www.biletix.com/static/images/live/event/eventimages/teoman_harbiye.jpg"
    eg8.save()
    
    event_groups = EventGroup.objects.all()
    
    datetimenow = datetime.datetime.now()
    
    event_places = ["Küçük Çiftlik Park", 'Park Orman','İTÜ Stadyum', 'TİM Maslak', 'Jolly Joker', 'Vişnelik', 'IF','Jolly Joker','Saklıkent']
    event_cities = [istanbul, istanbul, istanbul, istanbul, izmir, ankara, ankara, ankara, ankara]
    
    events = []
    for i in range(0,30):
        random_place = randrange(0,len(event_places))
        random_event_group = randrange(0,len(event_groups))
        e1 = Event()
        e1.eventGroup = event_groups[random_event_group]
        e1.place = event_places[ random_place ]
        e1.city = event_cities[ random_place ]
        e1.date = datetimenow + datetime.timedelta(days = randrange(20,100))
        
        random_seat_category_count = randrange(0,6)
        random_seat_row_count = randrange(1,15)
        
        if random_seat_category_count:
            for i in range(0,random_seat_category_count):
                e1.addSeatCategory( chr( i + ord('A') ) )
                
            for i in range(1,random_seat_row_count):
                    e1.addSeatRow( str(i) )
                

        
        e1.save()
        events.append(e1)

    users = []
    for i in range(0,25):
        u1 = User()
        u1.username = ''.join(random.choice(string.ascii_lowercase) for x in range(4,10)) + '@gmail.com'
        u1.gsm = '+90' + ''.join(random.choice(string.digits) for x in range(10))
        u1.address = 'some address'
        u1.iban = ''.join(random.choice(string.digits) for x in range(16))
        u1.saleCount = randrange(0,50)
        u1.purchaseCount = randrange(0,50)
        u1.save()
        users.append(u1)
    
    tickets = []
    seat_categories = ['A','B','C']
    for i in range(0,100):
        user_random = randrange(0,len(users))
        event_random = randrange(0,len(events))
        seat_category_random = randrange(0,len(seat_categories))
        
        t1 = Ticket()
        t1.user = users[user_random]
        t1.event = events[event_random]
        t1.price = randrange(25,200)
        t1.creationDate = datetimenow + datetime.timedelta(days = randrange(-10,0))
        t1.ticketCount = randrange(1,6)
        t1.seatCategory = seat_categories[seat_category_random]
        t1.save()
        
