# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime, timedelta, time
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
today = datetime.now().date()
class UserManager(models.Manager):

    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['name_error'] = "First and Last must be 2 or more characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        if len(postData['password']) < 8 or len(postData['confirm_password']) < 8:
            errors['pass_length'] = "Password must be 8 or more characters"
        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = "Passwords must match"
        if User.objects.filter(email=postData['email']):
            errors['exists'] = "Email already taken"
        return errors
    
    def login(self, postData):
        errors = {}
        user_to_check = User.objects.filter(email=postData['email'])
        if len(user_to_check) > 0:
            user_to_check = user_to_check[0]
            if bcrypt.checkpw(postData['password'].encode(), user_to_check.password.encode()):
                user = {"user" : user_to_check}
                return user
            else:
                errors = { "error": "Login Invalid" }
                return errors
        else:
            errors = { "error": "Login Invalid" }
            return errors
class ActivityManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if not postData['date']:
			errors['no_date'] = 'No date entered'
        if not postData['time']:
			errors['no_time'] = 'No time entered'

        # elif:
        if not datetime.strptime(postData['date'],  "%Y-%m-%d").date() >= today:
            errors['date_error'] = 'Date cannot be before today\'s date'

        if len(postData['title']) < 2:
            errors['title_error'] = "Title must be 2 or more characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Activity(models.Model):
    DURATION_CHOICES=(
        ('Days', 'Days'),
        ('Hours', 'Hours'),
        ('Minutes', 'Minutes'),
    )
    title = models.CharField(max_length=255)
    time = models.TimeField()
    date = models.DateField()
    duration_number = models.IntegerField()
    duration = models.CharField(max_length=200, choices=DURATION_CHOICES, default='Hours')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="event_coordinator")
    number_of_participants = models.ManyToManyField(User, related_name="participants")
    objects = ActivityManager()