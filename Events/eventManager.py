from Events.models import Event

def insertEvent(name, description):
    e = Event(name,description)
    e.save()

def insertEventt():
    e = Event(name='konser',description='cok hos')
    e.save()    

def getAllEvents():
    return Event.objects.all()
    