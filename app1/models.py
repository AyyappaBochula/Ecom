from django.db import models

# Create your models here.

class Customer(models.Model):
    cid=models.AutoField(primary_key=True)
    f_name=models.CharField(max_length=30)
    l_name=models.CharField(max_length=30)
    username=models.CharField(max_length=30,unique=True)
    password=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    mobile_no=models.CharField(max_length=15,unique=True)
    def __str__(self):
        return str(self.cid)+self.username+self.email+self.mobile_no

class Category(models.Model):
    name=models.CharField(max_length=30,unique=True)
    sizes=models.JSONField(default=list)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    pid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    price=models.FloatField()
    on_sale=models.BooleanField(default=False)
    sale_price=models.FloatField(null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    desc=models.TextField(max_length=250)
    image=models.ImageField(upload_to='products/',null=True,blank=True)
    
    @property
    def current_price(self):
        if(self.on_sale):
            return self.sale_price
        else:
            return self.price
    def __str__(self):
        return f'{self.category}-{self.name}-{self.current_price}'
    

class Cart(models.Model):
    customer=models.OneToOneField(Customer,on_delete=models.CASCADE)
    products=models.JSONField(default=list)

    @property
    def total_price(self):
        total=0
        for i in self.products:
            a=i['price']*i['quantity']
            total+=a
        return total
    def __str__(self):
        return f"{self.customer.username}---->{len(self.products)}"

class Order(models.Model):
    oid=models.AutoField(primary_key=True)
    status_choices=[('pending','pending'),('delivered','delivered')]
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    products=models.JSONField(default=list)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=15,choices=status_choices,default='pending')
    @property
    def total_price(self):
        total=0
        for i in self.products:
            a=i['price']*i['quantity']
            total+=a
        return total
    
    def __str__(self):
        return f'{self.customer.f_name}--{self.status}'
