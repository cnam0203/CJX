from django.db import models
from django.apps import apps

# Create your models here.

class Channel_Type(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return str(self.name)

class Source_Type(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return str(self.name)

class Device_Browser(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return str(self.name)

class Device_OS(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return str(self.name)

class Device_Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return str(self.name)

class Interact_Item_Type(models.Model):
    company_items = [model for model in apps.all_models['company_items']]
    company_items.remove('customer')
    company_items_choices = [(item, item) for item in company_items]
    name = models.CharField(max_length=50, blank=True, null=True, unique=True, choices = company_items_choices)

    def __str__(self):
        return str(self.name)

class Experience_Emotion(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return str(self.name)
        


class Action_Type(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return str(self.name)

class Journey_Customer(models.Model):
    customerID  = models.BigIntegerField(blank=False, null=True, unique=True)
    register_date = models.DateTimeField(auto_now=True)

class Touchpoint(models.Model):
    customer_id            = models.BigIntegerField(blank=False, null=True)
    action_type            = models.ForeignKey(Action_Type, blank=False, null=True, on_delete=models.SET_NULL)
    visit_time             = models.DateTimeField(blank=False, null=True)
    channel_type           = models.ForeignKey(Channel_Type, blank=True, null=True, on_delete=models.SET_NULL)
    device_browser         = models.ForeignKey(Device_Browser, blank=True, null=True, on_delete=models.SET_NULL)
    device_os              = models.ForeignKey(Device_OS, blank=True, null=True, on_delete=models.SET_NULL)
    device_category        = models.ForeignKey(Device_Category, blank=True, null=True, on_delete=models.SET_NULL)
    geo_continent          = models.CharField(max_length=50, blank=True, null=True)
    geo_country            = models.CharField(max_length=50, blank=True, null=True)
    geo_city               = models.CharField(max_length=50, blank=True, null=True)
    source_name            = models.ForeignKey(Source_Type, blank=True, null=True, on_delete=models.SET_NULL)
    source_url             = models.CharField(max_length=100, blank=True, null=True)
    ad_url                 = models.CharField(max_length=100, blank=True, null=True)
    ad_content             = models.CharField(max_length=100, blank=True, null=True)
    campaign_url           = models.CharField(max_length=100, blank=True, null=True)
    campaign_content       = models.CharField(max_length=100, blank=True, null=True)
    store_id               = models.BigIntegerField(blank=True, null=True)
    store_address          = models.CharField(max_length=100, blank=True, null=True)
    employee_id            = models.BigIntegerField(blank=True, null=True)
    webpage_id             = models.BigIntegerField(blank=True, null=True)
    webpage_url            = models.CharField(max_length=200, blank=True, null=True)
    webpage_title          = models.CharField(max_length=200, blank=True, null=True)
    app_screen_id          = models.BigIntegerField(blank=True, null=True)
    app_name               = models.CharField(max_length=50, blank=True, null=True)
    app_screen             = models.CharField(max_length=50, blank=True, null=True)
    app_screen_title       = models.CharField(max_length=50, blank=True, null=True)
    interact_item_type     = models.ForeignKey(Interact_Item_Type, blank=True, null=True, on_delete=models.SET_NULL)
    interact_item_id       = models.BigIntegerField(blank=True, null=True)
    interact_item_url      = models.CharField(max_length=100, blank=True, null=True)
    interract_item_content = models.CharField(max_length=500, blank=True, null=True)
    experience_score       = models.FloatField(blank=True, null=True)
    experience_emotion     = models.ForeignKey(Experience_Emotion, blank=True, null=True, on_delete=models.SET_NULL)
    record_time            = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_id}, {self.visit_time}, {self.action_type}, {self.channel_type}, {self.device_category}, {self.source_name}, {self.experience_emotion}"
    
    def save(self, *args, **kwargs):
        #figure out warranty end date
        if Journey_Customer.objects.filter(customerID=self.customer_id).exists() == False:
            Journey_Customer.objects.create(customerID=self.customer_id, register_date=self.visit_time)
        # else:
        #     journey_customer = Journey_Customer.objects.get(customerID=self.customer_id)
        #     if (journey_customer.register_date > self.visit_time):
        #         journey_customer.register_date = self.visit_time
        #         journey_customer.save()
        super(Touchpoint, self).save()



class Matching_Report(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True, unique=True)
    instruction_link = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Matching_Column(models.Model):
    functions = [(function, function) for function in ['lower', 'upper', 'datetime', 'string', 'int', 'float']]
    report = models.ForeignKey(Matching_Report, blank=False, null=True, on_delete=models.SET_NULL)
    journey_column = models.CharField(max_length=50, blank=False, null=True)
    report_column = models.CharField(max_length=50, blank=True, null=True)
    function = models.CharField(max_length=50, blank=True, null=True, choices=functions)


