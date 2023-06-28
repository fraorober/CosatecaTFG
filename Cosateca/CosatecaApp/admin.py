from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Person)
admin.site.register(Product)
admin.site.register(Booking)
admin.site.register(Availability)
admin.site.register(MessengerService)
admin.site.register(Rating)
admin.site.register(Report)
admin.site.register(WishList)
admin.site.register(ProductsInList)
admin.site.register(Verification)

