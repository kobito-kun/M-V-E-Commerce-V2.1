from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField()
	description = models.TextField(blank=True, null=True)
	digital = models.BooleanField(default=True, null=True, blank=False)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

class Order(models.Model):
	product_name = models.CharField(max_length=200, null=True, blank=True, default="Not Provided.")
	payer_email = models.EmailField(max_length=256, null=True, blank=True, default="Not Provided")
	complete = models.BooleanField(default=False, null=True, blank=True)
	date = models.DateField(auto_now_add= True, blank=True, null=True)
	transaction_id = models.CharField(max_length=200, null=True, blank=True, default="Not Provided.")
	product_id = models.IntegerField(default=0)	
	total_price = models.FloatField(default=0)
	paypal_order_id = models.CharField(max_length=200, default="Not Provided")

	def __str__(self):
		return self.payer_email

class Information(models.Model):
	company_name = models.CharField(max_length=200, default="Not Provided")	
	discord_webhook = models.URLField(max_length=300)
	paypal_client = models.CharField(max_length=200)
	paypal_client_secret = models.CharField(max_length=200, default="Not Provided")
	email_template_title = models.CharField(max_length=200)
	email_template_body = models.TextField(blank=True)
	gmail_host_address = models.EmailField(max_length=256)
	gmail_host_password = models.CharField(max_length=200)
	icon = models.URLField(max_length=200)

	def __str__(self):
		return self.company_name