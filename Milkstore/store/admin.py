from django.contrib import admin
from .models import Product,Category,cartitem,orderitem,Order,OTPverification # ✅ FIXED: Import Order from models

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(cartitem)
admin.site.register(orderitem)
admin.site.register(Order)
admin.site.register(OTPverification)

# Register your models here.
