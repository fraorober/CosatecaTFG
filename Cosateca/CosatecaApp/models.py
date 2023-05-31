from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Person(models.Model):
    
    address = models.CharField(max_length=40)
    postalCode = models.CharField(max_length=5)
    imageProfile = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=9)   #Falta validar
    banned = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person', default='null', null=False)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    

class Category(models.TextChoices):
    
    DEPORTES = "DEPORTES"
    MAQUINARIA = "MAQUINARIA"
    HERRAMIENTAS = "HERRAMIENTAS"

class Product(models.Model):
    
    name = models.CharField(max_length=60, blank=False, null=False)
    image = models.ImageField(upload_to="productos", null=True, blank=True)
    description = models.CharField(max_length=500, blank=False, null=False)
    category = models.CharField(Category, choices=Category.choices, max_length=12)
    publicationDate = models.DateField(auto_now_add=True ,blank=False, null=False)
    userWhoUploadProduct = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + ' added in ' + self.publicationDate.strftime('%d-%m-%Y') + ' by ' + self.userWhoUploadProduct.user.username
    
class Booking(models.Model):
    
    user = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    startDate = models.DateField(null=False, blank=False)
    endDate = models.DateField(null=False, blank=False)
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Object ' + self.product.name + 'is reserved from ' + self.startDate.strftime('%d-%m-%Y') + ' to the ' + self.endDate.strftime('%d-%m-%Y')
    
class Availability(models.Model):
    
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    busyDate = models.DateField(null=False, blank=False)
    
    def __str__(self):
        return 'Object ' + self.product + 'is booked on the ' + self.busyDate
    
class MessengerService(models.Model):
    
    sendDate = models.DateTimeField(null=False, blank=False)
    sender = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Person, related_name='receiver',null=False, on_delete=models.CASCADE)
    body = models.CharField(blank=False, max_length=1000)
    
    def __str__(self):
        return 'Message: ' + self.body + '. ' + self.sender.name + ' --> ' + self.receiver.name
    
class Rating(models.Model):
    
    rating = models.IntegerField()  #Validar min y max
    review = models.CharField(max_length=1000, null=True, blank=True)
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True )
    user = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Rating of ' + self.product.name + ' of ' + self.user.name + ': ' + str(self.rating)
    
class Reason(models.Model):
    
    reason = models.CharField(max_length=60, blank=False, null=False)
    
    def __str__(self):
        return self.reason

    
class Report(models.Model):
    
    date = models.DateField(null=False, blank=False)
    observations = models.CharField(max_length=300)
    reportedUser = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    reportingUser = models.ForeignKey(Person, null=False, related_name='reportingUser', on_delete=models.CASCADE)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
    capture = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return 'User ' + self.reportedUser.name + ' has been reported by ' + self.reportingUser.name
    
class WishList(models.Model):
    
    name = models.CharField(max_length=60, blank=False, null=False)
    owner = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class ProductsInList(models.Model):
    
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    wishList = models.ForeignKey(WishList, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return 'Product ' + self.product.name + ' added to list ' + "'" + self.wishList.name + "'"

class State(models.TextChoices):
    
    OPEN = "OPEN"
    INPROGRESS = "IN PROGRESS"
    CLOSED = "CLOSED"

class Verificaction(models.Model):
    
    userToVerify = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    video = models.URLField(blank=False, null=False)
    state = models.CharField(default=State.INPROGRESS, choices=State.choices, max_length=11)

    def __str__(self):
        return 'Verification ' + self.state + ' of ' + self.userToVerify.name
    




    
