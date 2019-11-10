from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
import random
from . models import Products, Views
import datetime
import decimal


def pick_randomY():
    randoms = [random.uniform(1.0, 1.49), random.uniform(
        1.4, 1.69), random.uniform(1.7, 1.89), random.uniform(1.9, 1.99)]
    weights = [0.4, 0.3, 0.2, 0.1]
    return round(random.choices(randoms, weights=weights)[0], 2)


def makeX():
    X_array = []
    for i in range(10):
        X_array.append(random.randint(1, 100))

    x = Views.objects.all()
    x0 = x[0]
    x0.X = X_array
    x0.save()


def makeY():
    Y_array = []
    for i in range(10):
        Y_array.append(pick_randomY())
    x = Views.objects.all()
    x0 = x[0]
    x0.Y = Y_array
    x0.save()

    # print(x[0].Y)


def minutesFromMidnight():
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    return seconds/60


def home(request):
    # global flag
    products = Products.objects.all()
    views = Views.objects.all()

    # caculate Days
    delta = (datetime.date.today()-products[0].dateUploaded)
    if delta.days == 0:
        Day = 1
    else:
        Day = delta.days + 1

    # if next day then change Y
    if datetime.date.today() != products[0].Daytimestamp:
        makeY()
        for product in products:
            product.Daytimestamp = datetime.date.today()
            product.save()

    # give minutes passed since last update
    delta = datetime.datetime.now(timezone.utc) - views[0].Viewtimestamp
    # print("now",datetime.datetime.now(timezone.utc))
    # print("view",views[0].Viewtimestamp)
    print("Seconds passed", delta.seconds)
    # if (delta.seconds)/60 >= 1:
    # print("view:before",views[0].Viewtimestamp)
    v0 = views[0]
    v0.Viewtimestamp = datetime.datetime.now(timezone.utc)
    v0.save()
    # print("view:after",views[0].Viewtimestamp)
    minutes_passed = (delta.seconds)/60

    for product in products:
        DummyView = Day * views[0].X[product.id-1] * views[0].Y[product.id-1]
        DummyViewPerMinute = (DummyView/(24*60))
        print("DummyViewsPerMinute", (DummyViewPerMinute) * minutes_passed)
        # print("minutes passed",delta.seconds/60)
        product.views += (minutes_passed * DummyViewPerMinute)
        product.save()
        print("product views",product.views)
    return render(request, '../templates/home.html', {'Products': products})


def productView(request, product_id):
    product = Products.objects.get(pk=product_id)
    product.views += 1
    product.save()
    return render(request, '../templates/productpage.html', {'product': product})
