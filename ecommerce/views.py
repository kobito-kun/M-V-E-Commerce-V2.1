from django.shortcuts import render
from django.conf.urls.static import static
from django.http import HttpResponseRedirect, HttpResponse
from datetime import date
import json
import requests
import smtplib
from .models import *

def viewCommerce(request):
    products = Product.objects.all()
    admin = Information.objects.get(id=1)
    context = {
        'products': products,
        'admin':admin
    }
    return render(request, 'index.html', context) 

def viewProduct(request, product_id):
    product = Product.objects.get(id=product_id)
    admin = Information.objects.get(id=1)    
    context = {
        'products': product,
        'admin':admin
    }
    return render(request, 'product.html', context)

def checkout(request, product_id):
    product = Product.objects.get(id=product_id)
    admin = Information.objects.get(id=1)
    context = {
        'products': product,
        'admin': admin
    }
    return render(request, 'checkout.html', context)

def paymentComplete(request):

    # GET Requests
    admin = Information.objects.get(id=1)
    body = json.loads(request.body)
    Id = body['productId']
    Email = body['email']
    Total = body['total']
    productName = body['name']
    orderID = body['orderID']
    Today = date.today()

    print('BODY:', body)
    print(Id)
    print(Email)
    print(Total)
    print(productName)
    print(Today)
    print(orderID)

    Order.objects.create(
        product_id = Id,
        complete = True,
        payer_email = Email,
        product_name = productName,
        total_price = Total,
        paypal_order_id = orderID,
        )

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(admin.gmail_host_address, admin.gmail_host_password)

    subject = 'Purchase Confirmation: ' + productName
    title = admin.email_template_title
    body = admin.email_template_body

    msg = f"Subject: {subject}\n\n{title}\n{body}"
    server.sendmail(
        'Order for: ' + productName,
        Email,
        msg
    )
    print("Sent Email")

    requests.post(admin.discord_webhook, json={
      "username": admin.company_name,
      "avatar_url": admin.icon,
      "embeds": [
        {
          "author": {
            "name": admin.company_name,
            "url": "",
            "icon_url": admin.icon
          },
          "title": "Order Complete",
          "url": "",
          "description": "A new order has been created for : " + "**" + productName + "**",
          "color": 15258703,
          "fields": [
            {
              "name": "Email: ",
              "value": Email,
            },
            {
              "name": "Order ID: ",
              "value": orderID,
              "inline": True
            },
            {
              "name": "Price Paid: ",
              "value": "$" + Total,
              "inline": True
            },            
            {
              "name": "Gateway: ",
              "value": "PayPal",
            },
          ],
          "footer": {
            "text": "Purchase date: " + Today.strftime("%d/%m/%Y"),
            "icon_url": admin.icon
          }
        }
      ]
    })
    print("Sent Webhook")
    return HttpResponseRedirect(request, 'complete.html')
