from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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
    
    SPORTS = "SPORTS"
    MACHINERY = "MACHINERY"
    TOOLS = "TOOLS"
    GARDENING = "GARDENING"
    VIDEOGAMES = "VIDEOGAMES"
    CONSOLES = "CONSOLES"
    BOOKS = "BOOKS"
    PCs = "PCs"
    TABLETS = "TABLETS"
    MOBILE_PHONE = "MOBILE PHONE"
    ART = "ART"  

class Product(models.Model):
    
    name = models.CharField(max_length=60, blank=False, null=False)
    image = models.ImageField(upload_to="productos", null=True, blank=True)
    description = models.CharField(max_length=500, blank=False, null=False)
    category = models.CharField(Category, choices=Category.choices, max_length=12)
    publicationDate = models.DateField(auto_now_add=True ,blank=False, null=False)
    userWhoUploadProduct = models.ForeignKey(Person, related_name='whoUpload', null=False, on_delete=models.CASCADE)
    userWhoRentProduct = models.ForeignKey(Person, related_name='whoRent', null=True, on_delete=models.CASCADE)
    availab = models.BooleanField(default=True)

    
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
    
    rating = models.FloatField(default=0, validators=[
            MaxValueValidator(5.0),
            MinValueValidator(0.0)
        ]
    )
    subject = models.CharField(max_length=100, blank=True)
    review = models.CharField(max_length=1000, null=True, blank=True)
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True )
    update_date = models.DateTimeField(auto_now=True )
    user = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Rating of ' + self.product.name + ' of ' + self.user.user.first_name + ': ' + str(self.rating)
    
class Reason(models.TextChoices):
    
    FRAUDULENT_BEHAVIOR  = "FRAUDULENT EHAVIOR"
    DAMAGE_OR_LOSS_OBJECTS = "DAMAGE OR LOSS OBJECTS"
    ILLEGAL_ACTIVITIES = "ILLEGAL ACTIVITIES"

    
class Report(models.Model):
    
    date = models.DateField(null=False, blank=False, auto_now_add=True)
    observations = models.CharField(max_length=300)
    reportedUser = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    reportingUser = models.ForeignKey(Person, null=False, related_name='reportingUser', on_delete=models.CASCADE)
    reason = models.CharField(Reason, choices=Reason.choices, max_length=25)
    capture = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return 'User ' + self.reportedUser.user.username + ' has been reported by ' + self.reportingUser.user.username
    
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
    




    
