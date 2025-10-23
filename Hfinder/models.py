# -*- coding: utf-8 -*-
from django.db import models

class Person(models.Model):
    registration_number = models.CharField(max_length=15)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    birth_date = models.DateField()
    email = models.EmailField()
    phone_number = models.IntegerField()
    password = models.CharField(max_length=32)
    friends = models.ManyToManyField('self')

    def __str__(self):
        return self.first_name+' '+self.last_name

class Message(models.Model):
    author = models.ForeignKey('Person', on_delete=models.CASCADE)
    content = models.TextField()
    publication_date = models.DateField()

    def __str__(self):
        if len(self.content)>20:
            return self.content[:19]+'...'
        else : 
            return self.content
