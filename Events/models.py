from django.db import models

class Event(models.Model):
    name = models.CharField(max_length = 30)
    description = models.CharField(max_length = 200)
    #photo_url
    #place
    #date & time
    #creation date
    
    def __unicode__(self):
            return self.name
