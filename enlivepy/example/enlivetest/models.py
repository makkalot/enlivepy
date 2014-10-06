from django.db import models

# Create your models here.
class TodoItem(models.Model):
    """
    Simple todo item here
    """
    name = models.CharField(max_length=100)
    done = models.BooleanField(default=False)


    def __unicode__(self):
        return u"-".join([self.name, str(self.done)])