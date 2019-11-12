from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
import random
from . models import Products, Views
import datetime
import decimal


# pick random Y with probabilty of 0.4, 0.3, 0.2, 0.1 in each set between [1.00,2.00)
def pick_randomY():
    randoms = [random.uniform(1.0, 1.49), random.uniform(
        1.4, 1.69), random.uniform(1.7, 1.89), random.uniform(1.9, 1.99)]
    weights = [0.4, 0.3, 0.2, 0.1]
    return round(random.choices(randoms, weights=weights)[0], 2)


# pick any value betweeen 1-100 with probablity 1/100 and make X array
def makeX():
    X_array = []
    for i in range(10):
        X_array.append(random.randint(1, 100))

    x = Views.objects.all()
    x0 = x[0]
    x0.X = X_array
    x0.save()

# make Y array using pick_randomY()
def makeY():
    Y_array = []
    for i in range(10):
        Y_array.append(pick_randomY())
    x = Views.objects.all()
    x0 = x[0]
    x0.Y = Y_array
    x0.save()


def home(request):
    products = Products.objects.all()
    views = Views.objects.all()

    # caculate Day (N)
    delta = (datetime.date.today()-products[0].dateUploaded)
    if delta.days == 0:
        if views[0].X == [0]*10:
            makeX()
        Day = 1
    else:
        Day = delta.days + 1


    # if next day then change Y
    if datetime.date.today() != products[0].Daytimestamp:
        makeY()
        for product in products:
            product.Daytimestamp = datetime.date.today()
            product.save()


    # give minutes passed since last update in views
    delta = datetime.datetime.now(timezone.utc) - views[0].Viewtimestamp
    v0 = views[0]
    v0.Viewtimestamp = datetime.datetime.now(timezone.utc)
    v0.save()
    minutes_passed = (delta.seconds)/60

    for product in products:

        # D = N * X * Y
        DummyView = Day * views[0].X[product.id-1] * views[0].Y[product.id-1]
        DummyViewPerMinute = (DummyView/(24*60))
        product.views += (minutes_passed * DummyViewPerMinute)
        product.save()
    return render(request, '../templates/home.html', {'Products': products})


def productView(request, product_id):
    # increase view if user visits a product
    product = Products.objects.get(pk=product_id)
    product.views += 1
    product.actualViews+=1
    product.save()
    return render(request, '../templates/productpage.html', {'product': product})


def dashboard(request):
    products = Products.objects.all()
    views = Views.objects.all()

    # caculate Day (N)
    delta = (datetime.date.today()-products[0].dateUploaded)
    if delta.days == 0:
        Day = 1
    else:
        Day = delta.days + 1
    
    viewsDict = {}
    for product in products:

            # D = N * X * Y
            DummyView = Day * views[0].X[product.id-1] * views[0].Y[product.id-1]
            productName = product.title
            actualView = product.actualViews
            viewsDict[productName] = DummyView + actualView
            
    return render(request,'../templates/dashboard.html',{'viewsDict':viewsDict})
