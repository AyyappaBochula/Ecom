from django.contrib import admin
from app1.models import Customer,Product,Cart,Order,Category
# Register your models here.
class Customer_Admin(admin.ModelAdmin):
    list_display=['cid','f_name','l_name','username','password','email','mobile_no']
admin.site.register(Customer,Customer_Admin)
class Category_Admin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Category,Category_Admin)
class Product_Admin(admin.ModelAdmin):
    list_display=['pid','name','price','on_sale','sale_price','category','desc','image']
admin.site.register(Product,Product_Admin)
class Cart_Admin(admin.ModelAdmin):
    list_display=['customer','products','total_price']
admin.site.register(Cart,Cart_Admin)
class Order_Admin(admin.ModelAdmin):
    list_display=['oid','customer','products','created_at','status','total_price']
admin.site.register(Order,Order_Admin)
