from django.db import models

# Create your models here.

class User(models.Model):  #Herencia abstracta
    
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=40, null=False)
    email = models.EmailField(unique=True)
    dni = models.CharField(max_length=9)   #Falta validar
    admin = models.BooleanField()

    def __str__(self):
        return self.username
    
    class Meta:
        abstract = True
    
class Person(User):
    
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    address = models.CharField(max_length=40)
    postalCode = models.IntegerField(max_length=99999)
    imageProfile = models.ImageField()
    phone = models.CharField(max_length=9)   #Falta validar
    banned = models.BooleanField(default=False)