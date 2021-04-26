from django.db import models

transaction_status_choices = [
    ("packaging", "packaging"), ("delivering", "delivering"), ("received", "received")]

class Customer(models.Model):
    username    = models.CharField(max_length=50, blank=True, null=True)
    password    = models.CharField(max_length=50, blank=True, null=True)
    email       = models.CharField(max_length=50, blank=True, null=True)
    dob         = models.DateField(max_length=50, blank=True, null=True)
    gender      = models.CharField(max_length=50, blank=True, choices=[("M", "M"), ("F", "F")])
    address     = models.CharField(max_length=50, blank=True, null=True)
    phone_number= models.CharField(max_length=50, blank=True)
    record_time = models.DateTimeField(auto_now=True)
    register_date = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name        = models.CharField(max_length=50, blank=True, null=True)
    category    = models.CharField(max_length=50, blank=True, null=True)
    price       = models.FloatField(blank=True, null=True)
    sku         = models.IntegerField(blank=True, null=True)
    promotion   = models.CharField(max_length=50, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class Post(models.Model):
    customer_id  = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    url         = models.CharField(max_length=50, blank=True, null=True)
    content     = models.CharField(max_length=50, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class Blog(models.Model):
    customer_id  = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    url         = models.CharField(max_length=50, blank=True, null=True)
    content     = models.CharField(max_length=50, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class Survey(models.Model):
    customer_id  = models.BigIntegerField(blank=True, null=True)
    url         = models.CharField(max_length=50, blank=True, null=True)
    content     = models.CharField(max_length=50, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)


class Campaign(models.Model):
    url         = models.CharField(max_length=50, blank=True, null=True)
    content     = models.CharField(max_length=50, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Review(models.Model):
    customer_id  = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    blog_id      = models.ForeignKey(Blog, null=True, on_delete=models.SET_NULL)
    url         = models.CharField(max_length=50, blank=True, null=True)
    content     = models.CharField(max_length=50, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    customer_id  = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    post_id      = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    url         = models.CharField(max_length=50, blank=True, null=True)
    content     = models.CharField(max_length=50, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Like(models.Model):
    customer_id  = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    post_id      = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    record_time = models.DateTimeField(auto_now=True)

class Rate(models.Model):
    customer_id  = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product_id   = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    rate_stars   = models.IntegerField()
    record_time = models.DateTimeField(auto_now=True)    

class Mail(models.Model):
    customer_id    = models.BigIntegerField(blank=True, null=True)
    url           = models.CharField(max_length=50, blank=True, null=True)
    content       = models.CharField(max_length=50, blank=True, null=True)
    record_time   = models.DateTimeField(auto_now=True)


class Advertisement(models.Model):
    url         = models.CharField(max_length=50, blank=True, null=True)
    content     = models.CharField(max_length=50, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Program(models.Model):
    url         = models.CharField(max_length=50, blank=True, null=True)
    content     = models.CharField(max_length=50, blank=True, null=True)
    record_time = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    customer_id  = models.BigIntegerField(blank=True, null=True)
    revenue     = models.FloatField(blank=True, null=True)
    shipping_fee = models.FloatField(blank=True, null=True)
    address     = models.CharField(max_length=50, blank=True, null=True)
    status      = models.CharField(
        max_length=50, blank=True, null=True, choices=transaction_status_choices)
    record_time = models.DateTimeField(auto_now=True)

