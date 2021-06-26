from django.db import models

class Timestamps(models.Model):
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)

 #Telling django not to create other db but add this field to child models
 class Meta:
  abstract = True