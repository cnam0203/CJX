from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _

from .models import Product
from .models import Transaction
from .models import Post
from .models import Blog
from .models import Review
from .models import Survey
from .models import Advertisement
from .models import Campaign
from .models import Program
from .models import Mail
from .models import Comment
from .models import Like
from .models import Rate
from .models import Customer

# Register your models here.

class Product_Admin(admin.ModelAdmin):
    search_fields = ("id", "name", "category", "price")
    list_display = ("id", "name", "category", "price", "sku", "promotion")

class Post_Admin(admin.ModelAdmin):
    list_display = ("id", "customer", "url", "content", "record_time")

    def customer(self, obj):
        link = "/admin/company_items/customer/" + str(obj.customer_id)
        return format_html("<a href='{}'>{}</a>", link, obj.customer_id)

class Blog_Admin(admin.ModelAdmin):
    list_display = ("id", "customer", "url", "content", "record_time")

    def customer(self, obj):
        link = "/admin/company_items/customer/" + str(obj.customer_id)
        return format_html("<a href='{}'>{}</a>", link, obj.customer_id)

class Campaign_Admin(admin.ModelAdmin):
    list_display = ("url", "content", "record_time")

class Review_Admin(admin.ModelAdmin):
    list_display = ("id", "customer", "blog", "url", "content", "record_time")

    def customer(self, obj):
        link = "/admin/company_items/customer/" + str(obj.customer_id)
        return format_html("<a href='{}'>{}</a>", link, obj.customer_id)

    def blog(self, obj):
        link = "/admin/company_items/blog/" + str(obj.blog_id)
        return format_html("<a href='{}'>{}</a>", link, obj.blog_id)

class Comment_Admin(admin.ModelAdmin):
    list_display = ("id", "customer", "post", "url", "content", "record_time")

    def customer(self, obj):
        link = "/admin/company_items/customer/" + str(obj.customer_id)
        return format_html("<a href='{}'>{}</a>", link, obj.customer_id)

    def post(self, obj):
        link = "/admin/company_items/post/" + str(obj.post_id)
        return format_html("<a href='{}'>{}</a>", link, obj.post_id)

class Like_Admin(admin.ModelAdmin):
    list_display = ("id", "customer", "post", "record_time")

    def customer(self, obj):
        link = "/admin/company_items/customer/" + str(obj.customer_id)
        return format_html("<a href='{}'>{}</a>", link, obj.customer_id)

    def post(self, obj):
        link = "/admin/company_items/post/" + str(obj.post_id)
        return format_html("<a href='{}'>{}</a>", link, obj.post_id)

class Rate_Admin(admin.ModelAdmin):
    list_display = ("id", "customer", "product", "rate_stars", "record_time")

    def customer(self, obj):
        link = "/admin/company_items/customer/" + str(obj.customer_id)
        return format_html("<a href='{}'>{}</a>", link, obj.customer_id)

    def product(self, obj):
        link = "/admin/company_items/product/" + str(obj.product_id)
        return format_html("<a href='{}'>{}</a>", link, obj.product_id)

class Survey_Admin(admin.ModelAdmin):
    list_display = ("id", "customer", "url", "content", "record_time")

    def customer(self, obj):
        link = "/admin/company_items/customer/" + str(obj.customer_id)
        return format_html("<a href='{}'>{}</a>", link, obj.customer_id)

class Mail_Admin(admin.ModelAdmin):
    list_display = ("id", "customer", "url", "content", "record_time")

    def customer(self, obj):
        link = "/admin/company_items/customer/" + str(obj.customer_id)
        return format_html("<a href='{}'>{}</a>", link, obj.customer_id)

class Advertisement_Admin(admin.ModelAdmin):
    list_display = ("id", "url", "content", "record_time")

class Program_Admin(admin.ModelAdmin):
    list_display = ("id", "url", "content", "record_time")

class Transaction_Admin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "revenue", "address", "record_time")

    def customer(self, obj):
        link = "/admin/company_items/customer/" + str(obj.customer_id)
        return format_html("<a href='{}'>{}</a>", link, obj.customer_id)

admin.site.register(Customer)
admin.site.register(Transaction, Transaction_Admin)
admin.site.register(Blog, Blog_Admin)
admin.site.register(Post, Post_Admin)
admin.site.register(Review, Review_Admin)
admin.site.register(Advertisement, Advertisement_Admin)
admin.site.register(Campaign, Campaign_Admin)
admin.site.register(Mail, Mail_Admin)
admin.site.register(Program, Program_Admin)
admin.site.register(Survey, Survey_Admin)
admin.site.register(Like, Like_Admin)
admin.site.register(Comment, Comment_Admin)



