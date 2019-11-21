from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=False)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    description = models.CharField(max_length=250)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'


class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    January = models.TextField()
    February = models.TextField()
    March = models.TextField()
    April = models.TextField()
    May = models.TextField()
    June = models.TextField()
    July = models.TextField()
    August = models.TextField()
    September = models.TextField()
    October = models.TextField()
    November = models.TextField()
    December = models.TextField()

