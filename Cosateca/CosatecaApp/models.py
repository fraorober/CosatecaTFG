from django.db import models

# Create your models here.

class User(models.Model):  #Herencia abstracta
    
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=40, null=False, blank=False)
    email = models.EmailField(unique=True, blank=False, null=False)
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
    postalCode = models.CharField(max_length=5)
    imageProfile = models.ImageField(null=True)
    phone = models.CharField(max_length=9)   #Falta validar
    banned = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name + ' ' + self.surname
    
class Category(models.Model):
    
    category = models.CharField(max_length=20)
    
    def __str__(self):
        return self.category

class Product(models.Model):
    
    name = models.CharField(max_length=60, blank=False, null=False)
    barcode = models.CharField(max_length=12, blank=False, null=False)
    image = models.ImageField()
    description = models.CharField(max_length=500, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publicationDate = models.DateField(blank=False, null=False)
    
    def __str__(self):
        return self.name
    
class Booking(models.Model):
    
    user = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    startDate = models.DateField(null=False, blank=False)
    endDate = models.DateField(null=False, blank=False)
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'El objeto ' + self.product + 'está reservado del ' + self.startDate + ' al ' + self.endDate
    
    